// pages/record/main.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        "type": " ",
        historyConversation: [
            {
                startTime:"04-08 16:23",
                status:"",
                counselor:{
                    avatar: "https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11",
                    name:"王咨询师"
                },
                duration:"6:23",
                evaluate:3, 
            },
            {
                startTime:"04-08 16:22",
                status:"",
                counselor:{
                    avatar: "https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11",
                    name:"王咨询师"
                },
                duration:"4:23",
                evaluate:4,
            },
            {
                startTime:"04-07 15:21",
                status:"",
                counselor:{
                    avatar: "https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11",
                    name:"王咨询师"
                },
                duration:"3:23",
                evaluate:1,
            }
        ]
    },

    onShow: function(){
        let model = getApp().globalData.model
        if(model){
          console.log("历史记录：", model)
          var items = JSON.parse(model);
          console.log("历史记录：",items)
          var self = this
          self.setData({
            historyConversation:items,
          });
        }
        else{
          console.log("没有历史记录")
        }
      }
})