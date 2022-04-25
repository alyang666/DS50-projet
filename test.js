const { spawn } = require('child_process');

//const childPython = spawn('python', ['comm.py']);

/**
 * js向python文件发送信息msg
 * (在python中读到的msg默认为string类型)
 */


/* node向py传输msg */
var msg = 1;
const childPython = spawn('python', ['Test.py', msg]);

/* 
// 传输JSON类型数据
obj = {Channel: 'nothing'}
const childPython = spawn('python', ['comm.py',JSON.stringify(obj)]);
*/

/* 读取python返回内容 */
childPython.stdout.on('data', (data) => {
    console.log("node to py :: ",data.toString());
});

/* 返回错误 */
childPython.stderr.on('data', (data) => {
    console.error(data.toString());
});

/* 返回python结束码 */
childPython.on('close', (code) => {
    console.log('child process exited with code : ',code.toString());
});


