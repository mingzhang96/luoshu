// first.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    option: '',
    bookList: [{}],
    containerShow: true,
    searchPanelShow: false,
    toastHidden: true,
    search_data: '',
    searchResult: [],
    detailData:[]
  },

  onBindFocus: function (event) {
    this.setData({
      containerShow: false,
      searchPanelShow: true
    })
  },

  onCancelImgTap: function (event) {
    this.setData({
      containerShow: true,
      searchPanelShow: false
    })
  },

  onStarImgTap: function (exent) {
    var that = this
    that.setData({
      toastHidden: false
    })
    return
  },

  toastChange: function () {
    this.setData({
      toastHidden: true
    })
  },

  onBindBlur: function (event) {
    var text = event.detail.value;
    var that = this;
    this.setData({
      search_data: text
    })
    var searchUrl = "http://139.199.20.193:8000/api/search?searchword=" + text + "&page=" + that.data.page;
    console.log(text);
    this.getsearchResult(searchUrl);
  },

  getsearchResult: function (url) {
    this.setData({
      containerShow: false,
      searchPanelShow: true
    })
    wx.showNavigationBarLoading();
    var that = this;
    wx.request({
      url: url,
      method: 'GET',
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        console.log(JSON.stringify(res));
        if(res.data.amount!='0'){
          var list = that.data.searchResult.concat(res.data.booklist)
          that.setData({
            searchResult: list
          })
          console.log(JSON.stringify(that.data.searchResult));
        }else{
          that.setData({
            toastHidden: false
          })
        }

        wx.hideNavigationBarLoading();
      },
      fail: function (error) {
        // fail
        console.log(error);
      }
    })
  },

  moredetail: function (event) {
    console.log(event.currentTarget.dataset.booksid)
    wx.navigateTo({
      url: './detail/detail?bookSid=' + event.currentTarget.dataset.booksid
    })
  },

  


  /**
   * 生命周期函数--监听页面加载
   */

  onLoad: function(option) {
    var that = this;
    this.setData({
      option: option,
      page: 1
    })
    wx.showNavigationBarLoading();
    wx.request({
      url: 'http://139.199.20.193:8000/api/getborrowranking',
      type: "GET",
      header: {
        "Content-Type": "json"
      },
      success: function (res) {
        that.setData({
          bookList: res.data.booklist
        })
        console.log(JSON.stringify(res))
      }
    })
    wx.hideNavigationBarLoading();
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
    var that = this;
    var page = that.data.page + 1;
    this.setData({
      page: page
    })
    that.getsearchResult("http://139.199.20.193:8000/api/search?searchword=" + text + "&page=" + page);
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