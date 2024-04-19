import os

import requests
from bs4 import BeautifulSoup
import urllib.request

from django.core.files import File
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from links.models import UserLink, UserLinkCollection
from links.serializers import UserLinkSerializer, UserLinkCollectionSerializer

from links.links_create_utils import cookies, headers


class CustomAutoSchema(SwaggerAutoSchema):
    """
    Customizing the tags in Swagger
    """
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'my_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


def links_list_retrieve_response():
    return {
            HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "title": openapi.Schema(type=openapi.TYPE_STRING),
                        "description": openapi.Schema(type=openapi.TYPE_STRING),
                        "url": openapi.Schema(type=openapi.TYPE_STRING),
                        "image": openapi.Schema(type=openapi.TYPE_STRING),
                        "link_type": openapi.Schema(type=openapi.TYPE_STRING),
                        "creation_date": openapi.Schema(type=openapi.TYPE_STRING),
                        "change_date": openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }


def link_collections_list_retrieve_response():
    return {
            HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "user_links": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER)
                    ),
                    "creation_date": openapi.Schema(type=openapi.TYPE_STRING),
                    "change_date": openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }


class UserLinkAPIViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints of user links
    """
    serializer_class = UserLinkSerializer
    permission_classes = (IsAuthenticated,)
    my_tags = ['Links']

    def get_queryset(self):
        user = self.request.user.id
        return UserLink.objects.filter(user=user)

    @swagger_auto_schema(
        operation_summary='Adding a link',
        operation_description='Add a link to the user base',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'link': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['link']
        ),
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                    "url": openapi.Schema(type=openapi.TYPE_STRING),
                    "link_type": openapi.Schema(type=openapi.TYPE_STRING),
                    "image": openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        response = requests.get(
            request.data['link'],
            cookies=cookies,
            headers=headers,
        )

        data = {'user_id': self.request.user.id}

        soup = BeautifulSoup(response.content, "html.parser")

        if soup.find("meta", property="og:title"):
            title = soup.find("meta", property="og:title")['content']
            data['title'] = title
        elif soup.find('title'):
            title = soup.find('title').text
            data['title'] = title

        if soup.find("meta", property="og:description"):
            description = soup.find("meta", property="og:description")['content']
            data['description'] = description
        elif soup.find("meta", {'name': 'description'}):
            description = soup.find("meta", {'name': 'description'})['content']
            data['description'] = description
        else:
            data['description'] = 'no description'

        if soup.find("meta", property="og:url"):
            url = soup.find("meta", property="og:url")['content']
            data['url'] = url
        else:
            data['url'] = request.data['link']

        if soup.find("meta", property="og:type"):
            link_type = soup.find("meta", property="og:type")['content']
            data['link_type'] = link_type
        else:
            data['link_type'] = 'website'

        if soup.find("meta", property="og:image"):
            image = soup.find("meta", property="og:image")['content']
            data['image'] = image
        else:
            data['image'] = 'https://i.postimg.cc/90WC7pzc/default.png'

        pic_path = data['image'].split('/')[-1].removesuffix('.png').replace('.', '') + '.png'
        urllib.request.urlretrieve(data['image'], pic_path)

        urls_querry = UserLink.objects.filter(user_id=self.request.user.id)
        urls_list = []
        for i in urls_querry.values('url'):
            urls_list.append(i['url'])
        if data['url'] in urls_list:
            return Response('The link is already in the collection')
        else:
            with open(pic_path, 'rb') as img_file:
                UserLink.objects.create(
                    user_id=data['user_id'],
                    title=data['title'],
                    description=data['description'],
                    url=data['url'],
                    link_type=data['link_type'],
                    image=File(img_file, name=pic_path)
                )
            os.remove(pic_path)
            return Response(data)

    @swagger_auto_schema(
        operation_summary='Links list',
        operation_description='Show all user links',
        responses=links_list_retrieve_response()
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Link by id',
        operation_description='Show user link by id',
        responses=links_list_retrieve_response()
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Updating a link',
        operation_description='Update a link in the user base',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "url": openapi.Schema(type=openapi.TYPE_STRING),
                "link_type": openapi.Schema(type=openapi.TYPE_STRING),
                "image": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title', 'description', 'url', 'link_type', 'image']
        ),
        responses=links_list_retrieve_response()
    )
    def update(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Partial updating a link',
        operation_description='Partial update a link in the user base',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "url": openapi.Schema(type=openapi.TYPE_STRING),
                "link_type": openapi.Schema(type=openapi.TYPE_STRING),
                "image": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses=links_list_retrieve_response()
    )
    def partial_update(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Deleting a link',
        operation_description='Delete a link from the user base',
    )
    def destroy(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        return super().destroy(request, *args, **kwargs)


class UserLinkCollectionAPIViewSet(viewsets.ModelViewSet):
    """
    Viewset for endpoints of user link collections
    """
    serializer_class = UserLinkCollectionSerializer
    permission_classes = (IsAuthenticated,)
    my_tags = ['Link Collections']

    def user_links_code(self, request):
        user = self.request.user.id
        link = UserLink.objects.filter(user_id=user)
        user_links_list = []
        for ul in link.values('id'):
            user_links_list.append(ul['id'])
        user_links = request.data['user_links']
        i = 0
        while i < len(user_links):
            if user_links[i] not in user_links_list:
                del user_links[i]
            else:
                i += 1
        return user, user_links

    def get_data(self, request):
        part = self.user_links_code(request)
        title = request.data['title']
        description = request.data['description']
        data = {
            'user': part[0],
            'user_links': part[1],
            'title': title,
            'description': description,
        }
        return data

    def get_queryset(self):
        user = self.request.user.id
        return UserLinkCollection.objects.filter(user=user)

    @swagger_auto_schema(
        operation_summary='Collections list',
        operation_description='Show all user collections',
        responses=link_collections_list_retrieve_response()
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Collection creation',
        operation_description='Creating a collection to group user links',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_links": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['user_links', 'title']
        ),
        responses={
            HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "user_links": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                 items=openapi.Schema(type=openapi.TYPE_INTEGER)
                                                 ),
                    "title": openapi.Schema(type=openapi.TYPE_STRING),
                    "description": openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        data = self.get_data(request)
        instance = UserLinkCollection.objects.create(
            user_id=data['user'],
            title=data['title'],
            description=data['description']
        )
        instance.user_links.set(data['user_links'])
        instance.save()

        return Response(data)

    @swagger_auto_schema(
        operation_summary='Collection by id',
        operation_description='Show user collection by id',
        responses=link_collections_list_retrieve_response()
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Updating a collection',
        operation_description='Update a collection to group user links in the user base',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_links": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['user_links', 'title', 'description']
        ),
        responses=link_collections_list_retrieve_response()
    )
    def update(self, request, *args, **kwargs):
        data = self.get_data(request)
        instance = UserLinkCollection.objects.get(id=kwargs['pk'])
        instance.user_id = data['user']
        instance.title = data['title']
        instance.description = data['description']
        for ul in data['user_links']:
            instance.user_links.add(ul)
        instance.save()

        return Response(data)

    @swagger_auto_schema(
        operation_summary='Partial updating a collection',
        operation_description='Partial update a collection to group user links in the user base',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user_links": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                "title": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses=link_collections_list_retrieve_response()
    )
    def partial_update(self, request, *args, **kwargs):

        instance = UserLinkCollection.objects.get(id=kwargs['pk'])
        if 'user_links' in request.data:
            part = self.user_links_code(request)
            for ul in part[1]:
                instance.user_links.add(ul)
        if 'title' in request.data:
            instance.title = request.data['title']
        if 'description' in request.data:
            instance.description = request.data['description']
        instance.save()

        return Response(request.data)

    @swagger_auto_schema(
        operation_summary='Deleting a collection',
        operation_description='Delete a collection to group user links from the user base',
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
