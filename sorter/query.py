from .file_parser import *
from datetime import datetime
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from .models import *
from decimal import Decimal
import os


def add_directory(path):
    path = path.replace('/', '\\')
    if DirectoryGraph.objects.filter(abs_path=path).count() > 0:
        return 'Directory_already_exists'
    try:
        dir = DirectoryGraph(abs_path=path, dir_name=path.split('\\')[-1])
        images = os.listdir(path)
        nodes = 0
        dir.save()
        blankflag = True
        for image in images:
            if (image.split(".")[-1]) in ['jpg', 'jpeg', 'png', 'svg', 'webp']: #TODO: изменить на проверку по content-type / try-except в pillow
                add_image(image, dir)
                blankflag = False
                nodes += 1

        if blankflag:
            dir.delete()
            return 'No_images'
        dir.full_edges = (nodes * (nodes - 1)) // 2
        dir.nodes = nodes
        dir.save()
        return dir
    except FileNotFoundError:
        return 'Wrong_path'
    except Exception as e:
        raise Exception(e)


def update_directory(directory):
    try:
        dir = DirectoryGraph.objects.get(pk=directory)
        images = os.listdir(dir.abs_path)
        image_urls = list(map(lambda img: img.image, dir.images.all()))
        add_nodes = 0
        add_edges = 0
        blankflag = True
        for image in images:
            if ((image.split(".")[-1]) in ['jpg', 'jpeg', 'png', 'svg', 'webp']): #TODO: изменить на проверку по content-type / try-except в pillow
                img_url = dir.abs_path+'/'+image
                if not img_url in image_urls:
                    add_image(image, dir)
                    add_nodes += 1
                else:
                    image_urls.remove(img_url)
        for del_img in ImageNode.objects.filter(image__in=image_urls).annotate(nodes_linked=Count('relateto')):
            del_img.delete()
            add_nodes -= 1
            add_edges -= del_img.nodes_linked
        nodes = dir.nodes + add_nodes
        dir.nodes = nodes
        dir.edges = dir.edges + add_edges
        dir.full_edges = (nodes * (nodes - 1)) // 2
        dir.save()
        return dir
    except Exception as e:
        raise Exception(e)


def get_directories():
    return DirectoryGraph.objects.all()


def log_error(request, method, error):
    err = ErrorLog(request=request, method=method, error=error)
    err.save()


def add_image(image, directory):
    img = ImageNode(image=(directory.abs_path+'/'+image), directory=directory, real_name=str(image))
    img.save()


def update_graph(nodes, edges):
    graph = DirectoryGraph.objects.get(pk=1)
    graph.nodes = nodes
    graph.edges = edges
    graph.fulledges = int(nodes*(nodes-1)/2)
    graph.save()


def update_img_rates(rates, directory):
    newedges = 0
    imageIds = list(map(lambda item: item.get('id'), rates.values()))
    items = dict(map(lambda item: (item.get('id'), {'rate': item.get('rate')}), rates.values()))
    for it in ImageNode.objects.filter(pk__in=imageIds):
        items[it.pk]['item'] = it
    for id, img in items.items():
        img['item'].compares += 1
        img['item'].sumrate += Decimal(img['rate'])
        img['item'].rate = Decimal(img['item'].sumrate / img['item'].compares)
        for j in rates.values():
            if j['id'] != id:
                if not (items[j['id']]['item'] in img['item'].relateto.all()):
                    print("SVYAz", j['id'], img['item'].id)
                    newedges += 1
                    img['item'].relateto.add(items[j['id']]['item'])
                    items[j['id']]['item'].relateto.add(img['item'])

        img['item'].save()
    graph = DirectoryGraph.objects.get(dir_name=directory)
    graph.edges += newedges
    graph.save()


def new_comparsion(dir_name):
    graph = DirectoryGraph.objects.get(dir_name=dir_name)
    allImages = ImageNode.objects.filter(directory=graph)
    allImages = allImages.annotate(nodes_linked=Count('relateto')).order_by('nodes_linked')
    i = 0
    needed = 5
    response_list = []
    while needed > 0 and i < allImages.count():
        if allImages[i].nodes_linked != (graph.nodes-1):
            if not allImages[i] in response_list:
                response_list.append(allImages[i])
            needed -= 1
            j = i+1
            while needed > 0 and j < allImages.count():
                if (not allImages[j] in allImages[i].relateto.all()) and (not allImages[j] in response_list):
                    response_list.append(allImages[j])
                    needed -= 1
                j += 1
        i += 1

    print("LEn", len(response_list))
    if len(response_list) == 0:
        "VSE BLYAT"
        return None
    else:
        return response_list
