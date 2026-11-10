const CryptoJS = require('crypto-js');
function GetSign(city) {
    var currentTime = new Date();
    var year = currentTime["getFullYear"]();
    var mon = currentTime['getMonth']() + 0x1;
    var day = currentTime['getDate']();
    var hour = currentTime['getHours']();
    var minute = currentTime['getMinutes']();
    var second = currentTime['getSeconds']();
    if (0xa > day) {
        day = '0' + day;
    }
    if (0xa > mon) {
        mon = '0' + mon;
    }
    if (0xa > hour) {
        hour = '0' + hour;
    }
    if (0xa > minute) {
        minute = '0' + minute;
    }
    if (0xa > second) {
        second = '0' + second;
    }
    var timeString = year + '' + mon + '' + day + '' + hour + '' + minute + '' + second;
    var data = city + '_' + timeString;
    let key = CryptoJS['enc']['Utf8']['parse']('5ha5Z7cZ3WNbD3rA');
    let iv = CryptoJS['enc']['Utf8']['parse']('AYk98XaiBwCi0Dst');
    let encryptData = CryptoJS['AES']['encrypt'](data, key, {
        'mode': CryptoJS['mode']['CBC'],
        'iv': iv,
        'padding': CryptoJS['pad']['Pkcs7']
    });
    sign = encryptData['toString']();
    return sign
}
var i=GetSign("xian")
console.log(i)

// 注意以上代码 是需要js的加密库crypto-js  安装需要执行两条命令  npm install crypto-js
// 如果出错修改文件夹（D:\Program Files\nodejs\node_cache 和D:\Program Files\nodejs\node_modules ）属性安全-全控制修改