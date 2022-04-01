// pages/counselor/main.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        isTiptrue: true,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (query) {
        let firstOpen = wx.getStorageSync("loadOpen")
        console.log("是否首次打开本页面==",firstOpen)
        if (firstOpen == undefined || firstOpen == '') { //根据缓存周期决定是否显示新手引导
          this.setData({
            isTiptrue: true,
          })
        } else {
          this.setData({
            isTiptrue: false,
          })
        }
     },
    closeThis(e){
        wx.setStorage({
          key: 'loadOpen',
          data: 'OpenTwo'
        })
        this.setData({
          isTiptrue:false
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
    onShow: function () {

    },

    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

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

    }
})