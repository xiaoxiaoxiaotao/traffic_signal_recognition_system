<template>
  <div>
    <h1 class="gradient-text">Traffic Sign Recognition</h1>
    <link href="https://fonts.googleapis.com/css?family=Archivo+Black&display=swap" rel="stylesheet">

    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="About The Team" name="first">
        <p>
          <div><b>Front-end:</b> Hu lifan, Li songtao, Meng Deyu</div>
          <div><b>Back-end:</b> Li Songtao, Tang Disen</div>
          <div><b>Algorithms and models:</b> Li zhaorui, Wang Lisheng</div>
        </p>
        <p>
          <div><b>If you need our src:</b><a href="https://github.com/xiaoxiaoxiaotao/traffic_signal_recognition_system" target="_blank">please click here!</a>.</div>
        </p>
      </el-tab-pane>

      <el-tab-pane label="About the project" name="second">
        <h3>Project description</h3>
        <p>
          Our Vision based sign detection system for autonomous vehicles is a software product that uses cameras to identify traffic signs on roads and guide vehicles to make different responses to different traffic signs. The purpose of this prototype is to train a data set of a region through deep learning, upload the images captured by the camera and process them to get the correct results. The product needs to carry out automatic image loading and processing cycle functions. In addition, the prototype needs to react to different image signs to deal with different road conditions. This feature will help drivers make appropriate decisions in advance, helping to reduce the accident rate and congestion rate of the transportation system. The ultimate goal of the prototype is to develop a fully autonomous driving system. Can be commercialized and used by the transportation industry and related customers.
        </p>
      </el-tab-pane>

      <el-tab-pane label="Path to the impact and challenges" name="third">
        <h3>Goal</h3>
        <p>
          We are committed to creating a product that has the functionality to assist traffic drivers in proper vehicle driving operations. This could potentially help transportation systems to become more efficient and reduce the probability of traffic accidents. These may make our products competitive in the market. Also, this product may have a positive impact on establishing a networked digital transportation system. However, in order to ensure that the product has the performance required by the market, we will face and solve some expected challenges. First, in order for the product to be broadly adaptable to traffic systems, we need to build a large database of traffic signs to support the algorithms in getting the results we want. Second, the product needs to utilize image recognition and deep learning in Python algorithms. These require a certain level of technical skills from the team members. What’s more, the positioning in market of this product requires the accuracy of the product's algorithms in order to avoid traffic hazards associated with erroneous results. To achieve this goal, we plan to conduct round robin testing and collect feedback data. Based on this, we will realize the correct image recognition and processing functions. In addition, in order to achieve the function of driving assistance, we require the product to have low latency of information interaction, which requires us to optimize the product algorithm and network transmission. Finally, in order to be competitive in the market, our product needs a good UI interface to facilitate the use of the product. In addition to the above challenges, we may encounter anticipated unexpected challenges during the product development phase. However, we believe that our team has good communication skills and ability to work as a perfect team. We are confident to cope with the unknown challenges. Meanwhile, we will keep improving our product to cope with our needs. We will carry forward the spirit of unity and dedication, which supports our expectation of getting a good enough product.
        </p>
      </el-tab-pane>

      <el-tab-pane label="Future" name="fourth">
        <p>If you have some suggestions for us, please contact with our best captain: <b>Li Zhaorui</b></p>
        <div><b>The phone number:</b> 13137148798</div>
        <div><b>The email:</b> 1823292890@qq.com</div>
        <br>
      </el-tab-pane>
    </el-tabs>
    <hr>

    <el-radio-group v-model="tabPosition" style="margin-bottom: 30px;">
    </el-radio-group>
    <el-tabs :tab-position="tabPosition" style="height: 600px;">
      <el-tab-pane label="Photo upload">
                <!-- 新增的输出框 -->
                <div  class="output-box">
          <h3>Server Response:</h3>
          <p>{{ serverResponse }}</p>
        </div>
        <el-upload
          id="img_upload"
          class="upload-demo"
          action="https://jsonplaceholder.typicode.com/posts/"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :file-list="fileList"
          :before-upload="beforeAvatarUpload"
          list-type="picture"
        >

          <el-button slot="trigger" size="large" type="primary">Please click here to pick the picture.</el-button>
          <el-button style="margin-left: 10px;" size="large" type="success" @click="PhotoUpload">Upload</el-button>
           <!--
          <el-button style="margin-left: 10px;" size="large" type="success" @click="test">test</el-button>
          -->

          <label for="rid_temp">rid</label>
          <input type="text" id="rid_temp" v-model="rid" />
          <div slot="tip" class="el-upload__tip">only the jpg files，no more than 2MB</div>
        </el-upload>
        <p id="info"></p>
        <!-- 缩略图区域 -->
        <div class="thumbnails">
          <h3>Thumbnails</h3>
          <div v-for="file in fileList" :key="file.name" class="thumbnail">
            <img :src="file.thumbnailSrc" alt="Thumbnail" v-if="file.thumbnailSrc">
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="Camarea">
           <!-- 新增的输出框 -->
        <div  class="output-box">
          <h3>Server Response:</h3>
          <p>{{ serverResponse }}</p>
        </div>
        <div id="camarea">
          <video ref="video" width="320" height="240" autoplay></video>
          <div>
            <!--先省略了两个button，已实现了opencamarea后自动截取和上传
            <el-button @click="snapPhoto">Snap Photo</el-button>
            <el-button @click="savePhoto">Save Photo</el-button>
            -->
            <el-button @click="openCamera" type="primary">Open Camera</el-button>
          </div>
          <!--隐藏的第二个屏幕
          <canvas ref="canvas" width="320" height="240"></canvas>
          -->
          <canvas ref="canvas" :class="{ hidden: !isCanvasVisible }" width="320" height="240"></canvas>
          <div>
            <el-button @click="stopCamera" value="Stop" >Stop</el-button>
          </div>

        </div>
      </el-tab-pane>
    </el-tabs>

  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: 'first',
      fileList: [],
      timer: null,
      tabPosition: 'left',
      rid: '',
      serverResponse: '' // 新增的属性
    };
  },
  methods: {
    test(){
    	let data={
    		"1231":"123"
    	}
      const xhr = new XMLHttpRequest();
      xhr.open('POST', 'http://127.0.0.1:8000/test', true);
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          console.log(response);
        }
      };
      xhr.send(JSON.stringify(data));
    },

    handleClick(tab, event) {
      console.log(tab, event);
    },
    handleRemove(file, fileList) {
      console.log(file, fileList);
      this.fileList = fileList;
    },
    handlePreview(file) {
      console.log(file);
      this.createThumbnail(file);
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传图片只能是 JPG 格式!');
      }
      if (!isLt2M) {
        this.$message.error('上传图片大小不能超过 2MB!');
      }
      if (isJPG && isLt2M) {
        this.createThumbnail(file);
      }
      return isJPG && isLt2M;
    },
    createThumbnail(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const imageData = e.target.result;
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        const thumbnailWidth = 200; // 缩略图宽度
        const thumbnailHeight = 200; // 缩略图高度

        const image = new Image();
        image.onload = () => {
          const scale = Math.min(thumbnailWidth / image.width, thumbnailHeight / image.height);
          canvas.width = image.width * scale;
          canvas.height = image.height * scale;

          context.drawImage(image, 0, 0, canvas.width, canvas.height);

          const thumbnailSrc = canvas.toDataURL('image/jpeg');

          // 更新 fileList 中的对应文件
          this.fileList.push({
            name: file.name,
            url: URL.createObjectURL(file),
            thumbnailSrc: thumbnailSrc,
            raw: file,
          });
        };
        image.src = imageData;
      };
      reader.readAsDataURL(file);
    },
    PhotoUpload() {
    if (this.fileList.length === 0) {
      this.$message.error('Please select a file first!');
      return;
    }

  const rid = this.rid;
  if (!rid) {
    this.$message.error('Please enter the rid!');
    return;
  }

    const file = this.fileList[this.fileList.length - 1].raw;
    this.submitBlob(file, rid);
    },

    submitBlob(file, rid) {
      const formData = new FormData();
      formData.append('picture', file, file.name);
      formData.append('rid', rid);

      const xhr = new XMLHttpRequest();
      const url = 'http://127.0.0.1:8000/upload/';
      xhr.open('POST', url, true);

      xhr.onerror = function() {
        console.error('Request error');
      };

      xhr.onload = () => {
        let response = JSON.parse(xhr.responseText);
        console.log(response.code);
        if (xhr.status === 200) {
          const result = JSON.parse(response.result);
          console.log(Object.keys(result))
          this.serverResponse = 'Shangchuan chenggong！\nFuwuqi geichu de jieguo shi：' + JSON.parse(result.result0).max_result;
        } else {
          this.serverResponse = 'Shangchuan shibai！\nFuwuqi fanhui：' + response.msg;
        }
      };

      console.log('Uploading to:', url);
      console.log('FormData:', formData);
      xhr.send(formData);
    },

    snapPhoto() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');

      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => {
        this.convertBlobToJPG(blob).then((jpgBlob) => {
          const formData = new FormData();
          formData.append('picture', jpgBlob, 'photo.jpg');
          formData.append('rid', this.rid); // 将rid添加到formData中

          const xhr = new XMLHttpRequest();
          xhr.open('POST', 'http://127.0.0.1:8000/upload/', true);
          xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
              const response = JSON.parse(xhr.responseText);
              document.getElementById('info').innerText = response.message;
            }
          };
          xhr.send(formData);
        });
      }, 'image/jpeg');
    },
    convertBlobToJPG(blob) {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (event) => {
          const img = new Image();
          img.onload = () => {
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            context.drawImage(img, 0, 0);
            canvas.toBlob((jpgBlob) => {
              resolve(jpgBlob);
            }, 'image/jpeg');
          };
          img.src = event.target.result;
        };
        reader.readAsDataURL(blob);
      });
    },
    savePhoto() {
      const canvas = this.$refs.canvas;
      const dataURL = canvas.toDataURL('image/jpeg');
      const blob = this.dataURLtoBlob(dataURL);
      const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });

      this.fileList.push({
        name: 'photo.jpg',
        url: URL.createObjectURL(file),
        raw: file,
      });
    },
    dataURLtoBlob(dataURL) {
      const byteString = atob(dataURL.split(',')[1]);
      const mimeString = dataURL.split(',')[0].split(':')[1].split(';')[0];
      const buffer = new ArrayBuffer(byteString.length);
      const dataView = new Uint8Array(buffer);

      for (let i = 0; i < byteString.length; i++) {
        dataView[i] = byteString.charCodeAt(i);
      }

      return new Blob([buffer], { type: mimeString });
    },
    openCamera() {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          this.$refs.video.srcObject = stream;
          // 每0.5秒拍照并上传
          this.timer = setInterval(() => {
            this.snapPhoto();
            const canvas = this.$refs.canvas;
            const dataURL = canvas.toDataURL('image/jpeg');
            const blob = this.dataURLtoBlob(dataURL);
            this.submitBlob(blob, 1919810);

          }, 500);
        })
        .catch((error) => {
          console.error('Error opening camera:', error);
        });
    },
    stopCamera() {
      const video = this.$refs.video;
      const stream = video.srcObject;
      const tracks = stream.getTracks();

      tracks.forEach((track) => {
        track.stop();
      });

      // 清除定时器
      clearInterval(this.timer);
    }
  },
  mounted() {
    this.startFetching(); // 组件挂载时开始获取数据
  },
  beforeDestroy() {
    this.stopFetching(); // 组件销毁前停止获取数据
  }
};
</script>

<style scoped>
  /* Tutorial on https://fossheim.io/writing/posts/css-text-gradient. */

.gradient-text {
  /* Fallback: Set a background color. */
  background-color: #CA4246;
  
  /* Create the gradient. */
   background-image: linear-gradient(
        45deg,
        #CA4246 16.666%, 
        #E16541 16.666%, 
        #E16541 33.333%, 
        #F18F43 33.333%, 
        #F18F43 50%, 
        #8B9862 50%, 
        #8B9862 66.666%, 
        #476098 66.666%, 
        #476098 83.333%, 
        #A7489B 83.333%);
  
  /* Set the background size and repeat properties. */
  background-size: 100%;
  background-repeat: repeat;

  /* Use the text as a mask for the background. */
  /* This will show the gradient as a text color rather than element bg. */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; 
  
  /* Animate the text when loading the element. */
    /* This animates it on page load and when hovering out. */
    animation: rainbow-text-simple-animation-rev 0.75s ease forwards;

}

.gradient-text:hover{
    animation: rainbow-text-simple-animation 0.5s ease-in forwards;
}


/* Move the background and make it smaller. */
/* Animation shown when entering the page and after the hover animation. */
@keyframes rainbow-text-simple-animation-rev {
    0% {
        background-size: 650%;
    }
    40% {
        background-size: 650%;
    }
    100% {
        background-size: 100%;
    }
}

/* Move the background and make it larger. */
/* Animation shown when hovering over the text. */
@keyframes rainbow-text-simple-animation {
    0% {
        background-size: 100%;
    }
    80% {
        background-size: 650%;
    }
    100% {
        background-size: 650%;
    }
}
  


/* Style the rest of the page. */
body {
  background: #e8995d ;
}

header {
  margin-top: 1em;
  margin-top: calc(50vh - 3em);
}

h1 {
  font-family: "Archivo Black", sans-serif;
  font-weight: normal;
  font-size: 45px;
  text-align: center;
  margin-bottom: 0;
  margin-bottom: -0.25em;
  display: block;
  margin-left: auto;
  margin-right: auto;
  cursor: pointer;
  width: 605px;
}

p {
  font-family: "Helvetica Neue"
}

  #camarea {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  #camarea video, #camarea canvas {
    border: 2px solid #ccc;
    border-radius: 10px;
    margin-bottom: 10px;
  }
  .el-upload__tip {
    font-size: 16px;
    margin-top: 10px;
    color: #666;
  }
  .thumbnail img {
    width: 100px; /* 缩略图宽度 */
    height: auto;
    margin: 5px;
  }
  .hidden {
  display: none;
  }
  .output-box {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ffffff;
  border-radius: 5px;
  background-color: #f8ecd1;
}
</style>
