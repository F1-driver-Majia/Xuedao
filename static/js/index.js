new Vue({
    el: '#index1',
    data:{
        topmenu:[],
        banner:[],
        userUI:false,
        username:'',
        password:''
    },
    mounted(){

        this.getData()
    },
    methods:{
        getData:function () {
            var self = this
            // 避免指向错误
            reqwest({
                url:'/api/index',
                //在载入时从api中获取数据库数据
                methods: 'get',
                type: 'json',
                success: function (data) {
                    console.log(data)
                    self.topmenu = data.topmenu
                    self.banner = data.banner

                }
            })
        },
        userlogin:function(){
            var self = this
            reqwest({
                url:'/api/index',
                method:'post',
                type: 'json',
                data:{
                    username:self.username,
                    password:self.password
                },
                success:function () {
                    console.log('ok')
                },
            })
            self.userUI = false
        },
        showLogin:function () {
            this.userUI = !this.userUI
        }
    }
})