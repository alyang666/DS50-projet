const { spawn } = require('child_process');


//const childPython = spawn('python', ['comm.py']);



// itemid指游戏的app_id 当然此处也可以输入string类型的游戏名（由前端参数决定）
// num指推荐几个和该游戏相似的游戏(按相似度排名)
var item_id = 10;
var num = 2;
const childPython = spawn('python', ['TD-IDF.py', item_id, num]);

/* 
// 传输JSON类型数据
obj = {Channel: 'nothing'}
const childPython = spawn('python', ['comm.py',JSON.stringify(obj)]);
*/

/* 读取python返回内容 */
childPython.stdout.on('data', (data) => {
    console.log(data.toString());
});

/* 返回错误 */
childPython.stderr.on('data', (data) => {
    console.error(data.toString());
});

/* 返回python结束码 */
childPython.on('close', (code) => {
    console.log('child process exited with code : ',code.toString());
});


