// pages/informed_consent/main.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        seconds : 3,
        timer : null
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

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
        var _this2 = this;
        this.seconds = 3;

        this.timer = setInterval(function () {
            _this2.seconds -= 1;
                if (_this2.seconds === 0) {
                clearInterval(_this2.timer);
                }
        }, 1000);
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

    },

    closeThis(e){
        wx.redirectTo({
            url: '/pages/counselor/main',
        })
    }

})