// pages/record/main.js
const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        "type": " ",
        historyConversation: [],
    },
    onLoad: function(){
        var that = this;
        //header = {'cookie':wx.getStorageSync("token")};
        var cookienow = app.globalData.mycookie;
        console.log(cookienow)
        wx.request({
          url: 'http://123.57.45.27:8022/visitor/weChat/conversation/',
          method: "GET",
          header : {'cookie': cookienow},
          success: function(res){
              console.log("res:"+ res.data.historyConversation[0].evaluate);
              console.log("res:"+ res.data.historyConversation[0].consultants.name);
              that.setData(
                {
                    historyConversation: res.data.historyConversation
                }
              )
              console.log("history:"+that.data.historyConversation[0].evaluate);
          },
        fail: function() {
          console.log('咨询记录获取失败');
          }
        })
    }

 })