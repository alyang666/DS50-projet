const { spawn } = require('child_process');


//const childPython = spawn('python', ['comm.py']);

/* 
// 传输JSON类型数据
obj = {Channel: 'nothing'}
const childPython = spawn('python', ['comm.py',JSON.stringify(obj)]);
*/


/**
 * 此处是与TD-IDF算法联调部分!!!!!!
 * itemid指游戏的app_id 当然此处也可以输入string类型的游戏名（由前端参数决定）
 * num指推荐几个和该游戏相似的游戏(按相似度排名)
 */
var item_id = 10;
var num = 2;
const childPython = spawn('python', ['TD-IDF.py', item_id, num]);
// 读取python返回内容 
childPython.stdout.on('data', (data) => {
    console.log(data.toString());
});
// 返回错误 
childPython.stderr.on('data', (data) => {
    console.error(data.toString());
});
// 返回python结束码 
childPython.on('close', (code) => {
    console.log('child process exited with code : ',code.toString());
});




/**
 * 与content_base算法联调部分!!!!!!
 * 传入参数只有游戏名
 */
var game_name = "Counter-Strike: Source"
const child_2 = spawn('python', ['Content.py', game_name]);

child_2.stdout.on('data', (data) => {
    console.log(data.toString());
});









