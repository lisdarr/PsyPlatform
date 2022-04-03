// pages/counselor/main.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        Consultants:[
            {
                gender:"女",
                userName:"cy",
                isConsulted:"咨询过",
                rate:"3",
                status:"空闲",
            },
            {
                gender:"女",
                userName:"cy",
                isConsulted:"咨询过",
                rate:"3",
                status:"空闲",
            },
            {
                gender:"女",
                userName:"cy",
                isConsulted:"咨询过",
                rate:"3",
                status:"空闲",
            },
            {
                gender:"女",
                userName:"cy",
                isConsulted:"咨询过",
                rate:"3",
                status:"空闲",
            }
        ],
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function () {
      
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