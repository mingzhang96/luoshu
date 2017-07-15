// borrow_info.js
Page({

  /**
   * 页面的初始数据
   */

  data: {
    amount: 0,
    bookList: [{}],
    userid: '',
    userpassword: ''
  },

  bindXujie: function(event) {
    var that = this
    console.log(event.currentTarget.dataset.xuhao)
    wx.request({
      url: "http://139.199.20.193:8000/api/continueborrow",
      method: "POST",
      data: {
        username: that.data.userid,
        password: that.data.userpassword,
        number: event.currentTarget.dataset.xuhao
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      success: function (res) {
        console.log("success!");
        that.setData({
          xujie: res.data.xujie
        })
        console.log(JSON.stringify(res))
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      userid: options.inputnumber,
      userpassword: options.inputpassword
    })
    var that = this
    console.log("password = " + that.data.userpassword)
    wx.request({
      url: "http://139.199.20.193:8000/api/getborrowinfo",
      method: "POST",
      data: {
        username: that.data.userid,
        password: that.data.userpassword
      },
      header: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      success: function (res) {
        console.log("success!");
        that.setData({
          loading: false,
          bookList: res.data.booklist,
          amount: res.data.amount
        })
        console.log(JSON.stringify(res))
        
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