// pages/record/main.js
Page({

    /**
     * 页面的初始数据
     */
    data: {
        "type": " ",
        historyConversation: [
            {
                startTime:"2021-11-17 16:23:23",
                status:"",
                counselor:{
                    gender:"男",
                    name:"gyy"
                },
                duration:"16:23:23",
                evaluate:3,
            },
            {
                startTime:"2021-11-17 16:23:23",
                status:"WAITING",
                counselor:{
                    gender:"女",
                    name:"cy"
                },
                duration:"34:23:34",
                evaluate:4,
            },
            {
                startTime:"2021-11-17 16:23:23",
                status:"WAITING",
                counselor:{
                    gender:"女",
                    name:"wrc"
                },
                duration:"14:23:34",
                evaluate:2,
            },
            {
                startTime:"2021-11-17 16:23:23",
                status:"WAITING",
                counselor:{
                    gender:"男",
                    name:"xsh"
                },
                duration:"14:23:34",
                evaluate:4,
            }
        ]
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {

    },

    handleScroll(){

    },
    handleRecord(){

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