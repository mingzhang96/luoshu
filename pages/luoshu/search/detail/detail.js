// detail.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading: false,
    bookSid: '',

    bookName: '',
    bookSummary: '',
    bookAuthor: '',
    bookPublisher: '',
    bookImage: '',

    toastHidden: true,
    isbn: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      bookSid: options.bookSid,
    })
    var that = this
    wx.request({
      url: "http://139.199.20.193:8000/api/getbookdetial?sid=" + that.data.bookSid,
      type: "GET",
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        that.setData({
          isbn: res.data.ISBN_ISSN
        })
        wx.request({
          url: "https://api.douban.com/v2/book/isbn/" + that.data.isbn,
          type: "GET",
          header: {
            "Content-Type": "json"
          },
          success: function (res) {
            that.setData({
              bookName: res.data.title + res.data.alt_title,
              bookSummary: res.data.summary,
              bookAuthor: res.data.author[0],
              bookPublisher: res.data.publisher,
              bookImage: res.data.images.small
            })
            console.log(JSON.stringify(res))
          }
        })
        console.log(JSON.stringify(res))

      }
    })
  },

  toastChange: function () {
    this.setData({
      toastHidden: true
    })
  },

  onStarImgTap: function (exent) {
    var that = this
    that.setData({
      toastHidden: false
    })
    wx.setStorage({
        bookName: event.currentTarget.dataset.bookName, 
        bookSummary: event.currentTarget.dataset.bookSummary
      })
    return
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