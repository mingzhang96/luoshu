// borrow.js
//获取应用实例
var app = getApp()
Page({
  data: {
    focus: false,
    inputnumber: '',
    inputpassword: '',
    toastHidden: true,
    loading: false,
    auth: false
  },
  toastChange: function () {
    this.setData({
      toastHidden: true
    })
  },
  bindSearchNumberInput: function (e) {
    this.setData({
      inputnumber: e.detail.value
    })
  },
  bindSearchPasswordInput: function (e) {
    this.setData({
      inputpassword: e.detail.value
    })
  },
  //事件处理函数
  bindSearchTap: function () {
    var that = this
    if ((that.data.inputnumber == null || that.data.inputnumber == "") && (that.data.inputpassword == null || that.data.inputpassword == "")) {
      console.log("请输入正确的学号和密码")
      that.setData({
        toastHidden: false
      })
      return
    }
    that.setData({
      loading: true
    })
    wx.request({
      url: "http://139.199.20.193:8000/api/auth",
      method: "POST",
      data: {
        username: that.data.inputnumber,
        password: that.data.inputpassword
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      success: function (res) {
        that.setData({
          loading: false
        })
        console.log(JSON.stringify(res))
        if(res.data["auth"] === "true"){
          console.log(res.data["auth"])
          wx.navigateTo({
            url: './borrow_info/borrow_info?inputnumber=' + that.data.inputnumber + '&inputpassword=' + that.data.inputpassword
          })
        }else{
          that.setData({
            toastHidden: false
          })
        }
      }
    })
    that.setData({
      loading: false
    })
  },

  json2Form: function(json) {  
    var str = [];  
    for(var p in json){  
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(json[p]));
    }
    return str.join("&");  
  }  
})