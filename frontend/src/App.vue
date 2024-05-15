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
        <el-upload
      class="upload-demo"
      action="https://jsonplaceholder.typicode.com/posts/"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :file-list="fileList"
      :before-upload="beforeAvatarUpload"
      list-type="picture"
    >
      <el-button slot="trigger" size="large" type="primary">Please click here to pick the picture.</el-button>
      <el-button style="margin-left: 10px;" size="large" type="success" @click="submitUpload">Upload</el-button>
      <label for="rid_temp">rid</label>
      <input type="text" id="rid_temp"/>
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
      <div id="camarea">
      <video ref="video" width="320" height="240" autoplay></video>
      <div>
      <el-button @click="snapPhoto">Snap Photo</el-button>
      <el-button @click="savePhoto">Save Photo</el-button>
      <el-button @click="openCamera">Open Camera</el-button>
      </div>
      <!--第二个屏幕-->
      <canvas ref="canvas" width="320" height="240"></canvas>
      <div>
      <el-button @click="stopCamera" value="Stop">Stop</el-button>
      </div>
      
      <!--原按钮，更改统一样式后不确定是否会导致功能变化
      <input type="button" @click="stopCamera" value="Stop">
      -->

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
      tabPosition: 'left'
    };
  },
  methods: {
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
    uploadPicture() {
      const fileInput = document.getElementById('file-input');
      const file = fileInput.files[0];
      const rid = document.getElementById('rid_temp').value;

      const formData = new FormData();
      formData.append('picture', file);
      formData.append('rid', rid);

      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/upload', true);
      xhr.onload = function() {
        const response = JSON.parse(xhr.responseText);
        console.log(response.code);
        if (xhr.status === 200) {
          alert('上传成功！\n服务端给出结果是：' + response.result);
        } else {
          alert('上传失败！\n服务端答道：' + response.msg);
        }
      };
      xhr.send(formData);
    },
  
  


    submitUpload() {
      this.$refs.upload.submit();
    },
    openCamera() {
      this.loadCamera();
    },
    loadCamera() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
          video.srcObject = stream;
          video.play();
          this.timer = setInterval(() => {
            context.drawImage(video, 0, 0, 320, 240);
            this.sendCanvasToServer();
          }, 500);
        }).catch((error) => {
          console.error('Error accessing camera:', error);
        });
      }
    },
    sendCanvasToServer() {
      const canvas = this.$refs.canvas;
      const imageData = canvas.toDataURL('image/jpeg');

      const canvasData = {
        imageData: imageData
      };

      fetch('http://localhost:8000', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(canvasData)
      })
        .then((response) => {
          if (response.ok) {
            console.log('Canvas data sent successfully.');
          } else {
            console.error('Failed to send canvas data.');
          }
        })
        .catch((error) => {
          console.error('Error sending canvas data:', error);
        });
    },
    snapPhoto() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, 320, 240);
    },
    savePhoto() {
      const canvas = this.$refs.canvas;
      const image = canvas.toDataURL('image/png').replace('image/png', 'image/octet-stream');
      const tmpLink = document.createElement('a');
      tmpLink.download = 'image.png';
      tmpLink.href = image;
      document.body.appendChild(tmpLink);
      tmpLink.click();
      document.body.removeChild(tmpLink);
    },
    stopCamera() {
      clearInterval(this.timer);
    }
  }
};
</script>

<style>
body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen",
        "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue",
        sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

code {
    font-family: source-code-pro, Menlo, Monaco, Consolas, "Courier New",
        monospace;
}

.App {
    text-align: center;
}

.App-logo {
    height: 40vmin;
    pointer-events: none;
}

.App-header {
    position: static;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #0dc4e4;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: calc(16px + 2vmin);
    color: white;
}

.App-main {
    position: static;
    left: 0;
    width: 100%;
    background-color: #0cc3b0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: calc(10px + 2vmin);
    color: black;
}

.App-link {
    color: #61dafb;
}

.star {
    color: #f2ff00;
}

.small {
    font-size: 0.75rem;
}

.thumbnail {
  margin-top: 20px;
}

.thumbnail img {
  max-width: 100%;
}

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
  background-color: #fdf1f0;
}

header {
  margin-top: 1em;
  margin-top: calc(50vh - 3em);
}

h1 {
  font-family: "Archivo Black", sans-serif;
  font-weight: normal;
  font-size:45px;
  text-align: center;
  margin-bottom: 0;
  margin-bottom: -0.25em;
  display: block;
  margin-left: auto;
  margin-right: auto;
  cursor: pointer;
  width: 605px;
}
</style>