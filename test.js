const { spawn } = require('child_process');


//const childPython = spawn('python', ['comm.py']);

/* 
// 传输JSON类型数据
obj = {Channel: 'nothing'}
const childPython = spawn('python', ['comm.py',JSON.stringify(obj)]);
*/


/**
 * Connect nodejs with TD-IDF method
 * @param itemid : id of game (app_id in DB) 
 * @param num : the number of recommended games
 */
/*

var item_id = 10;
var num = 5;
const childPython = spawn('python', ['TD-IDF.py', item_id, num]);
// read return value of python
childPython.stdout.on('data', (data) => {
    console.log(data.toString());
});

/*
// return the error 
childPython.stderr.on('data', (data) => {
    console.error(data.toString());
});

// return the exit code of python
childPython.on('close', (code) => {
    console.log('child process exited with code : ',code.toString());
});
*/




/**
 * Connect with Content based method
 * @param game_name 
 * @param num : the number of recommended games
 */

var game_id = 12100;
var num = 8;
const child_2 = spawn('python', ['content.py', game_id, num]);


// read return value of python
child_2.stdout.on('data', (data) => {
    console.log(data.toString());
});



/**
 * Connect with Collaborative_filtering method
 * There are currently no input parameters
 */
/*
const child_3 = spawn('python', ['Collab_filtering.py']);

child_3.stdout.on('data', (data) => {
    console.log(data.toString());
});

*/

