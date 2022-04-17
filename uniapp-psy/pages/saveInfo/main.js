// index.js
// 获取应用实例
const app = getApp()

var username = ""
var phon_number = ""
var sos_name = ""
var sos_phon_number = ""

Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    canIUseGetUserProfile: false,
    canIUseOpenData: wx.canIUse('open-data.type.userAvatarUrl') && wx.canIUse('open-data.type.userNickName') // 如需尝试获取用户信息可改为false
  },
  getNameInput(e){
    username = e.detail.detail.value
    console.log("username",username)
  },
  getNumInput(e){
    phon_number = e.detail.detail.value
    if(phon_number.length == 11){
      this.checkNum(phon_number)
    }
    else return;
  },
  getSosNameInput(e){
    sos_name = e.detail.detail.value
    if(sos_name == username){
      wx.showToast({
        title: '紧急联系人姓名需不同，请修改',
        icon:'none',
        duration: 2000,
      })
    }
  },
  getSosNumInput(e){
    sos_phon_number = e.detail.detail.value
    if(sos_phon_number.length == 11){
      this.checkNum(sos_phon_number)
    }
  },
  checkNum(num){
    if(!/^[1][3,4,5,7,8][0-9]{9}$/.test(num)){
      wx.showToast({
        title: '号码不正确',
        icon:'error',
        duration: 2000,
      })
    }
    return;
  },
    handleProxy1(){
    //     wx.request({
    //       url: 'http://localhost:8000/admin/weChat/login/',
    //       method:"POST",
    //       data:{
    //         username: username,
    //         phon_number: phon_number,
    //         sos_name: sos_name,
    //         sos_phon_number: sos_phon_number
    //       },
    //       success: function(res){
    //         console.log('注册信息提交成功');
    //         console.log('注册 res:'+res);
    //         let gettoken = res.data.data.token;
    //         wx.setStorageSync("token","gettoken");
    //         console.log('token:'+token)
    //       },
    //       fail: function() {
    //         console.log('注册信息提交失败');
    //       }
    //     })
        wx.switchTab({
          url: '/pages/index/main',
        })
      },

  onLoad() {
    if (wx.getUserProfile) {
      this.setData({
        canIUseGetUserProfile: true
      })
    }
  }
})