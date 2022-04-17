// pages/record/main.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        "type": " ",
        historyConversation1:[],
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
    // onLoad: function(){
    //     var that = this;
    //     header = {'cookie':wx.getStorageSync("token")};
    //     wx.request({
    //       url: 'url',
    //       method: "GET",
    //       success: function(res){
    //           console.log("咨询记录 res:"+res);
    //           that.setData(
    //             {
    //                 historyConversation1: res.data.xxx   根据具体的res.data内容赋值给historyConversation1
    //             }
    //           )
    //       },
    //     fail: function() {
    //       console.log('咨询记录获取失败');
    //       }
    //     })
    // },

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