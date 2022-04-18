// pages/counselor/main.js
import IMService from "../../static/lib/imservice";
import restapi from "../../static/lib/restapi";

const app = getApp()

Page({

    /**
     * 页面的初始数据
     */
    data: {
        // currentUser: {
        //         uuid:'123',
        //         name:'cymm',
        //         avatar: "/static/images/Avatar-1.png"
        // },
        Consultants:[],
        // Consultants:[
        //     {
        //         gender:"男",
        //         userName:"王咨询师",
        //         isConsulted:"",
        //         rate:"3.4",
        //         status:"空闲",
        //         icon:"https://i03piccdn.sogoucdn.com/0354d6ffc3ecbe11"
        //     }
        // ],
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function () {
        var that = this;
        //console.log("全局mycookie:"+app.globalData.mycookie)
        var cookienow = app.globalData.mycookie;
        //console.log("咨询师cookienow："+cookienow)
        wx.request({
          url: 'http://123.57.45.27:8022/consultant/weChat/choice/',
          method: "GET",
          header : {'cookie':cookienow},
          success: function(res){
              console.log("咨询师 res.data.consultList[0].avator :"+res.data.consultList[0].avator);
              that.setData(
                {
                    Consultants : res.data.consultList
                }
              )
              console.log("咨询师 that.data.Consultants[0].name :"+that.data.Consultants[0].name);
              console.log("咨询师 that.data.Consultants[0].status :"+that.data.Consultants[0].status);
          },
        fail: function() {
          console.log('咨询师获取失败');
          }
        })
    },
    
    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    // onShow () {
    //     let that = this
    //     let currentUser = that.currentUser
    //     console.log(currentUser)
	// 	if(!currentUser){
	// 		wx.redirectTo({
	// 			url : '../index/main'
	// 		});
	// 		return;
	// 	}
	// 	if (wx.goEasy.getConnectionStatus() === 'disconnected') {
	// 		app.globalData.service = new IMService(wx.goEasy,wx.GoEasy);
	// 		app.globalData.service.connect(currentUser);
	// 	}
	// 	wx.showLoading({title: '加载中',mask: true});
	// 	//监听会话列表变化
	// 	let self = this;
	// 	wx.goEasy.im.on(wx.GoEasy.IM_EVENT.CONVERSATIONS_UPDATED, (conversations) => {
	// 		// 设置tabBar未读消息总数以及conversation
	// 		self.renderConversations(conversations);
	// 	});
	// 	//加载会话列表
	// 	wx.goEasy.im.latestConversations({
	// 		onSuccess: function (res) {
	// 			let content = res.content;
	// 			self.renderConversations(content);
	// 			wx.hideLoading();
	// 		},
	// 		onFailed: function (error) {
	// 			wx.hideLoading();
	// 			console.log(e);
	// 		}
	// 	});
	// },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {
        wx.reLaunch({
            url: '/pages/index/main'
          })
      
    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },

    /**
     * 用户点击右上角分享
     */
    onShareAppMessage: function () {

    },
    toConsult: function(){
        wx.navigateTo({
          url: '/pages/chat/main',
        });
    }


    
})