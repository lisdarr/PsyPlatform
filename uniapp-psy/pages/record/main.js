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
      let model = getApp().globalData.historyConversation
      if(model){
        var items = JSON.parse(model);
        var self = this
        self.setData({
          historyConversation:items,
        });
      }
      else{
        console.log("没有历史记录")
      }
    },

 })