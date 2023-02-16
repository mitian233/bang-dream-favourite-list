<script lang="ts" setup>
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'
const handleClose = (done: () => void) => {
  ElMessageBox.confirm('确定要关闭吗？')
      .then(() => {
        done()
      })
      .catch(() => {
        // catch error
      })
}
</script>
<template>
  <div id="gird">
    <h1 style="margin-bottom: 30px">邦邦生涯个人喜好表</h1>
    <div class="grid grid-cols-6 gap-4 w-fit" style="padding: 0 20px 10px 20px">
      <div v-for="item in listItem" class="border-4 border-black rounded-xl bg-white h-40 w-40 relative">
        <div class="bg-white h-37 w-37">
          <div style="position: absolute;top: 0;left: 0;width: 100%;height: 100%;display: flex;justify-content: center;align-items: center">
            <div v-if="!item.imgExist">
              <p>{{item.musicTitle}}</p>
            </div>
            <div v-else>
              <img :src="item.img" :alt="item.musicTitle" crossorigin="anonymous">
              <p class="absolute bg-white top-1 right-1" style="text-align: right;font-size: 12px;border-radius: 5px">{{item.musicTitle}}</p>
            </div>
          </div>
        </div>
        <p class="absolute bg-white bottom-1.5 left-2" style="border-radius: 5px">{{ item.title }}</p>
      </div>
    </div>
    <div>
      <p style="font-size: 13px;color: gray;padding-bottom: 10px">Created with https://myfavouritelist.bangdream.moe</p>
    </div>
  </div>
  <el-dialog v-model="pickUpVisible" title="选择歌曲" width="30%" :before-close="handleClose" draggable>
    <span>选择单元格：</span>
    <el-select v-model="selectBoxIndex" class="m-2" placeholder="Select" size="large" filterable>
      <el-option v-for="item in listItem" :key="item.title" :label="item.title" :value="listItem.indexOf(item)"/>
    </el-select>
    <br/>
    <span>　选择乐曲：</span>
    <el-select v-model="selectValue" class="m-2" placeholder="Select" size="large" filterable>
      <el-option v-for="item in songsList" :key="item" :label="item['musicTitle']" :value="songsList.indexOf(item)"/>
    </el-select>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="pickUpVisible = false">取消</el-button>
        <el-button type="danger" @click="deleteItem(selectBoxIndex)">清除选中</el-button>
        <el-button type="primary" @click="editAndSave(selectBoxIndex,selectValue)">
          保存
        </el-button>
      </span>
    </template>
  </el-dialog>
  <div>
    <el-button @click="saveImg">生成图片</el-button>
    <el-button @click="editWindow">编辑</el-button>
    <el-button type="danger" @click="deleteAll">清除所有</el-button>
  </div>
  <el-dialog v-model="saveImgDialogVisible" title="图片生成记录" width="70%" v-loading="imgDialogLoading">
    <p>长按以保存</p>
    <div id="saveimagecanvas"></div>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="danger" @click="deleteRecord">删除生成记录</el-button>
        <el-button type="primary" @click="saveImgDialogVisible = false">关闭</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts">
import html2canvas from "html2canvas";
import axios from "axios";
import songsListRaw from '../assets/all.5.js'
const BASE_URL = 'https://api-mfl.bangdream.moe/'
export default {
  name: "songsListView",
  data() {
    return {
      listItem: [
        {imgExist: false, img: '',musicTitle:'', title: '最爱的'},
        {imgExist: false, img: '',musicTitle:'', title: '最惊艳的'},
        {imgExist: false, img: '',musicTitle:'', title: '最长情的'},
        {imgExist: false, img: '',musicTitle:'', title: '最有感触的'},
        {imgExist: false, img: '',musicTitle:'', title: '最有意义的'},
        {imgExist: false, img: '',musicTitle:'', title: '最讨厌的'},
        {imgExist: false, img: '',musicTitle:'', title: '效率最高的'},
        {imgExist: false, img: '',musicTitle:'', title: '影响我最深的'},
        {imgExist: false, img: '',musicTitle:'', title: '带新人入坑必推的'},
        {imgExist: false, img: '',musicTitle:'', title: '入坑玩的第一首'},
        {imgExist: false, img: '',musicTitle:'', title: '打的最后一首'},
        {imgExist: false, img: '',musicTitle:'', title: '协力必点的'},
        {imgExist: false, img: '',musicTitle:'', title: '最喜欢的歌词'},
        {imgExist: false, img: '',musicTitle:'', title: '最喜欢的编曲'},
        {imgExist: false, img: '',musicTitle:'', title: '最喜欢的吉他'},
        {imgExist: false, img: '',musicTitle:'', title: '最喜欢的贝斯'},
        {imgExist: false, img: '',musicTitle:'', title: '最喜欢的鼓点'},
        {imgExist: false, img: '',musicTitle:'', title: '最喜欢的键盘/弦乐'},
      ],
      songsList: [],
      selectBoxIndex: 0,
      selectValue: 0,
      dialogVisible: false,
      saveImgDialogVisible: false,
      pickUpVisible: false,
      imgDialogLoading: false,
    }
  },
  methods: {
    addImg(item, girdIndex) {
      console.log('addImg', item, girdIndex)
    },
    saveImg() {
      this.imgDialogLoading = true
      this.saveImgDialogVisible = true
      console.log('saveImg')
      html2canvas(document.querySelector("#gird"),{
        backgroundColor: "#ffffff",
        allowTaint: true,
        useCORS: true,
        scrollY: 0,
        scrollX: 0,
      }).then(canvas => {
        document.querySelector('#saveimagecanvas').appendChild(canvas).style.width = '100%'
      })
      this.imgDialogLoading = false
    },
    editWindow() {
      this.pickUpVisible = true
    },
    deleteItem(target) {
      this.listItem[target].musicTitle = ''
      this.listItem[target].imgExist = false
      this.listItem[target].img = ''
    },
    deleteAll() {
      for (let i = 0; i < this.listItem.length; i++) {
        this.listItem[i].musicTitle = ''
        this.listItem[i].imgExist = false
        this.listItem[i].img = ''
      }
    },
    deleteRecord() {
      const canvasDiv = document.getElementById("saveimagecanvas");
      while (canvasDiv.firstChild) {
        canvasDiv.removeChild(canvasDiv.firstChild);
      }
    },
    edit(target,value) {
      console.log(this.listItem[target].title,'是',this.songsList[value].musicTitle,this.songsList[value].musicId)
      this.listItem[target].musicTitle = this.songsList[value].musicTitle
      axios.get(BASE_URL + 'jacket/' + this.songsList[value].musicJacket+'-jacket.png').then(res => {
        if (res.status == 200) {
          this.listItem[target].imgExist = true
          this.listItem[target].img = BASE_URL + 'jacket/' + this.songsList[value].musicJacket+'-jacket.png'
        } else {
          this.listItem[target].imgExist = false
          this.listItem[target].img = ''
        }
      })

      //this.listItem[target].img = 'https://bestdori.com/assets/jp/musicjacket/musicjacket480_rip/assets-star-forassetbundle-startapp-musicjacket-musicjacket480-472_japari_park-jacket.png'
    }
    ,
    editAndSave(target,value) {
      this.edit(target,value)
      //this.pickUpVisible = false
    }
  },
  mounted() {
    for (let i = 0; i < 473; i++) {
      if (songsListRaw[i] == undefined) {
        continue
      } else {
        const json = {
          musicTitle: songsListRaw[i].musicTitle[0],
          musicId: i,
          musicJacket: songsListRaw[i].jacketImage[0]
        }
        this.songsList.push(json)
      }
    }
  }
}
</script>
<style scoped>
</style>