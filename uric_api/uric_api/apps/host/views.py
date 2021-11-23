from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from .models import HostCategory, Host
from .serializers import HostCategoryModelSeiralizer, HostModelSerializers
from rest_framework.permissions import IsAuthenticated
import xlwt
from rest_framework.views import APIView
from rest_framework.response import Response
from io import BytesIO
from .utils import read_host_excel_data
from django.http.response import HttpResponse
from django.utils.encoding import escape_uri_path


class HostCategoryListAPIView(ListAPIView, CreateAPIView):
    queryset = HostCategory.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id").all()
    serializer_class = HostCategoryModelSeiralizer
    permission_classes = [IsAuthenticated]


class HostModelViewSet(ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostModelSerializers
    permission_classes = [IsAuthenticated]


class HostExcelView(APIView):
    permission_classes = [IsAuthenticated]
    # 中间代码省略....

    def get(self,request):
        # 1 读取数据库数据
        all_host_data = Host.objects.all().values('id', 'category', 'name', 'ip_addr', 'port', 'username',
                                                  'description')

        # 2 写入excel并保存
        # 创建excel
        xls = xlwt.Workbook(encoding='utf-8')
        # 创建工作簿
        sheet = xls.add_sheet('主机数据列表')
        # 给工作簿首行写入表头
        sheet.write(0, 0, 'id')
        sheet.write(0, 1, 'category')
        sheet.write(0, 2, 'name')
        sheet.write(0, 3, 'ip_addr')
        sheet.write(0, 4, 'port')
        sheet.write(0, 5, 'username')
        sheet.write(0, 6, 'description')

        # 写入数据，从第一行开始
        excel_row = 1 # 因为表头已经占据了下标为1的首行，所以此处从下标1开始写入主机数据
        for host_obj in all_host_data:
            sheet.write(excel_row, 0, host_obj.get('id'))
            sheet.write(excel_row, 1, host_obj.get('category'))
            sheet.write(excel_row, 2, host_obj.get('name'))
            sheet.write(excel_row, 3, host_obj.get('ip_addr'))
            sheet.write(excel_row, 4, host_obj.get('port'))
            sheet.write(excel_row, 5, host_obj.get('username'))
            sheet.write(excel_row, 6, host_obj.get('description'))
            excel_row += 1

        # 将数据写入io数据流，不用在本地生成excel文件，不然效率就低了
        sio = BytesIO()
        xls.save(sio)
        sio.seek(0)

        # 3 将excel数据响应回客户端
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')

        # 3.1 文件名称中文设置
        response['Content-Disposition'] = 'attachment; filename={}'.format(escape_uri_path('主机列表数据.xls'))
        response.write(sio.getvalue())  # 必须要给response写入一下数据，不然不生效
        return response

    def post(self, request):
        """批量导入主机列表"""
        # 接受客户端上传的数据
        host_excel = request.data.get("host[]")
        default_password = request.data.get("default_password")

        # 把上传文件全部写入到字节流，就不需要保存到服务端硬盘了。
        sio = BytesIO()
        for i in host_excel:
            sio.write(i)

        data = read_host_excel_data(sio, default_password)

        return Response(data)
