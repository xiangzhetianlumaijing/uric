<template>
  <div class="console">
    <div id="terminal"></div>
  </div>
</template>

<script>
import { Terminal } from 'xterm'
export default {
  name: "Console",
  mounted() {
    this.show_terminal()
  },
  methods:{
    show_terminal(){
      // 初始化terminal窗口
      var term = new Terminal({
        rendererType: "canvas", //渲染类型
        rows: 40, //行数
        convertEol: true, // 启用时，光标将设置为下一行的开头
        scrollback: 100,   // 终端中的回滚量
        disableStdin: false, //是否应禁用输入。
        cursorStyle: 'underline', //光标样式
        cursorBlink: true, //光标闪烁
        theme: {
          foreground: '#ffffff', //字体
          background: '#060101', //背景色
          cursor: 'help',//设置光标
        }
      });

      // 建立websocket
      let ws = new WebSocket(`ws://api.uric.cn:8000/ws/ssh/${this.$route.params.id}/`);
      var keyWord = '';  // 拼接用户输入的内容
      let msg = ""
      // 监听接收来自服务端响应的数据
      ws.onmessage = function (event) {
        if (!keyWord){
          //所要执行的操作
          term.write(event.data);
        }else {
          keyWord=''
          // 对响应回来的数据进行一些加工处理，筛选出结果内容部分
          let a = event.data.replace(event.data.split('\r\n',1)[0],'');
          let b = a.split('\r\n',-1).slice(0,-1).join('\r\n');
          term.write('\r\n'+b)
        }
      }

      term.prompt = () => {
        term.write('\r\n');
        // term.write('\r\n$ ')
        msg = '';
      }

      term.onKey(e => {
        console.log(e)
        const ev = e.domEvent
        const printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey

        console.log('>>>>',ev.keyCode);
        if (ev.keyCode === 13) {
          // console.log(keyWord);
          // 按下回车键进行指令的发送
          ws.send(keyWord);

        } else if (ev.keyCode === 8) {
          // Do not delete the prompt
          if (term._core.buffer.x > 2) {
            term.write('\b \b')
          }
        } else if (printable) {
          term.write(e.key);
          keyWord += e.key
        }
      })

      term.open(document.getElementById('terminal'));

    }
  }
}
</script>

<style scoped>

</style>