// app.js
import GoEasy from './static/lib/goeasy-2.2.7.min';


App({
  data:{
    model: null,
  },
  globalData: {
    token: null,
  },

  onLaunch: function () {
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })

    wx.goEasy = GoEasy.getInstance({
        host:'hangzhou.goeasy.io',//应用所在的区域地址: [hangzhou.goeasy.io, 新加坡暂不支持IM，敬请期待]
        appkey: 'BC-a9e0b1b27564446d942734742f8cbf07',// common key
        modules:["im"]
    });
    wx.GoEasy = GoEasy;
},

  formatDate: function(time) {
    const date = new Date(time);
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const minute = date.getMinutes();
    return [month, day].map(this.formatNumber).join('-') + ' ' + [hour, minute].map(this.formatNumber).join(':');
  },

  formatNumber:function(n) {
    n = n.toString();
    return n[1] ? n : '0' + n;
  },
  globalData: {
    service: null,
  }
})
