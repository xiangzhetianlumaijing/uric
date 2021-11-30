from django.shortcuts import render, HttpResponse

# Create your views here.

from .serializers import HostModelSerializers, HostCategoryModelSeiralizer


def test(request):
    # 反序列化
    hms = HostCategoryModelSeiralizer(data={"name": "测试"})

    print(hms.is_valid())
    print("errors", hms.errors)
    return HttpResponse("测试成功")


# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import HostCategory, Host
from .serializers import HostCategoryModelSeiralizer, HostModelSerializers
from rest_framework.permissions import IsAuthenticated


class HostCategoryListAPIView(ListAPIView, CreateAPIView):
    """主机类别"""
    queryset = HostCategory.objects.filter(is_show=True, is_deleted=False).order_by("orders", "-id").all()
    serializer_class = HostCategoryModelSeiralizer
    permission_classes = [IsAuthenticated]


class HostModelViewSet(ModelViewSet):
    serializer_class = HostModelSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 重写qureyset方法，补充过滤主机列表参数，获取主机列表
        category_id = self.request.query_params.get("category", None)
        queryset = Host.objects
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        return queryset.all()
