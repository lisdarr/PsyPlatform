// pages/chat/chat.js
Page({
  data: {
    starIndex : 0,
    hiddenkey : true
  },
  // 星星函数
  onChange(e){
    const index = e.detail.index;
    this.setData({
        'starIndex' : index
    })
},
//点击咨询完成弹出评价框
  evaluate(){
    let that = this
    console.log("点击咨询完成前，hiddenkey的值是",that.data.hiddenkey)
    that.setData({
      hiddenkey:false
    })
    console.log("点击咨询完成后，hiddenkey的值是",that.data.hiddenkey)
  },
//点击评价的提交按钮结束本次会话
  submit(){
    wx.switchTab({
      url: '/pages/index/main',
    })
    let that = this
    console.log("点击提交前，hiddenkey的值是",that.data.hiddenkey)
    that.setData({
      hiddenkey:true
    })
    console.log("点击提交后，hiddenkey的值是",that.data.hiddenkey)
  },
  showEmoji(){
		this.setData({
			["emoji.show"]: true,
			["more.show"]: false,
			recordVisible: false
		});
		// 关闭手机键盘
		wx.hideKeyboard().then(console.log).catch(console.log);
  },
  showMore(){
		this.setData({
			["more.show"]: true,
			["emoji.show"]: false
		});
		// 关闭手机键盘
		wx.hideKeyboard().then(console.log).catch(console.log);
  },
	messageInputFocusin(){
		this.setData({
			["more.show"]: false,
			["emoji.show"]: false
		});
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