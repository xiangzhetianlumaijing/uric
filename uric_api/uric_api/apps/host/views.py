from rest_framework.generics import ListAPIView,CreateAPIView
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
    """主机信息"""
    queryset = Host.objects.all()
    serializer_class = HostModelSerializers
    permission_classes = [IsAuthenticated]