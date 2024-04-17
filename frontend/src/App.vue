<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">

      <el-tab-pane label="About The Team" name="first">
        <p>
        <div><b>Front-end:</b>Hu lifan , Li songtao</div>
        <div><b>Back-end:</b>Li Songtao , Tang Disen</div>
        <div><b>Algorithms and models:</b>Li zhaorui , Meng deyu , Wang Lisheng</div>
      </p>
      </el-tab-pane>

      <el-tab-pane label="About the project" name="second"><h3>Project description</h3><p>Our Vision based sign detection system for autonomous vehicles is a software product that uses 
cameras to identify traffic signs on roads and guide vehicles to make different responses to different 
traffic signs. The purpose of this prototype is to train a data set of a region through deep learning, 
upload the images captured by the camera and process them to get the correct results. The product 
needs to carry out automatic image loading and processing cycle functions. 
In addition, the prototype needs to react to different image signs to deal with different road 
conditions. This feature will help drivers make appropriate decisions in advance, helping to reduce 
the accident rate and congestion rate of the transportation system. The ultimate goal of the prototype 
is to develop a fully autonomous driving system. Can be commercialized and used by the 
transportation industry and related customers.</p></el-tab-pane>
      <el-tab-pane label="Path to the impact and challenges" name="third"><h3>Goal</h3><p>We are committed to creating a product that has the functionality to assist traffic drivers in
proper vehicle driving operations. This could potentially help transportation systems to become 
more efficient and reduce the probability of traffic accidents. These may make our products 
competitive in the market. Also, this product may have a positive impact on establishing a networked 
digital transportation system.
However, in order to ensure that the product has the performance required by the market, we 
will face and solve some expected challenges. First, in order for the product to be broadly adaptable 
to traffic systems, we need to build a large database of traffic signs to support the algorithms in 
getting the results we want. Second, the product needs to utilize image recognition and deep learning 
in Python algorithms. These require a certain level of technical skills from the team members. 
What’s more, the positioning in market of this product requires the accuracy of the product's 
algorithms in order to avoid traffic hazards associated with erroneous results. To achieve this goal, 
we plan to conduct round robin testing and collect feedback data. Based on this, we will realize the 
correct image recognition and processing functions. In addition, in order to achieve the function of 
driving assistance, we require the product to have low latency of information interaction, which
requires us to optimize the product algorithm and network transmission. Finally, in order to be 
competitive in the market, our product needs a good UI interface to facilitate the use of the product.
In addition to the above challenges, we may encounter anticipated unexpected challenges 
during the product development phase. However, we believe that our team has good communication 
skills and ability to work as a perfect team. We are confident to cope with the unknown challenges. 
Meanwhile, we will keep improving our product to cope with our needs. We will carry forward the 
spirit of unity and dedication, which supports our expectation of getting a good enough product.</p></el-tab-pane>
      <el-tab-pane label="Future" name="fourth">
        <p>If you have some suggestions for us, please contact with our best captain: <b>Li Zhaorui</b></p>
        <div><b>The phone number:</b>13137148798</div>
        <div><b>   The   email:</b>1823292890@qq.com</div>
        <br>
      </el-tab-pane>
    </el-tabs>
    <hr>
    <el-upload
    class="upload-demo"
    action="https://jsonplaceholder.typicode.com/posts/"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :file-list="fileList"
    :before-upload="beforeAvatarUpload"
    list-type="picture">
    <el-button slot="trigger" size="large" type="primary" id="file-input">Please click here to pick the picture.</el-button>
    <el-button style="margin-left: 10px;" size="large" type="success" onclick="uploadPicture()" id="upload">Upload</el-button>
    <label for="rid_temp">rid</label>
    <input type="text" id="rid_temp"/>
    <div slot="tip" class="el-upload__tip">only the jpg files，no more than 2MB</div>
    </el-upload>
    <p id="info"></p>

        

  </div>
  </template>
  <script>
    export default {
      data() {
        return {
          activeName: 'first',
          fileList: [{name: 'food.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100',src:''}, {name: 'food2.jpeg', url: '', src:''}],
    
        };
      },
      methods: {
        handleClick(tab, event) {
          console.log(tab, event);},

        handleRemove(file, fileList) {
        console.log(file, fileList);},
        handlePreview(file) {
        console.log(file);},
        
        beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;
          
        if (!isJPG) {
          this.$message.error('上传图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },

      submitUpload() {
        this.$refs.upload.submit();
      },
      }
    };


    window.onload = function() {
    let fileInput = document.getElementById('file-input');
    let preview = document.getElementById('uploaded-image');
    let info = document.getElementById('info');
    // listen change event:
    fileInput.addEventListener('change', function() {
        // clear previous image:
        preview.style.backgroundImage = '';
        if (!fileInput.value) {
            info.innerHTML = '没有选择文件';
            return;
        }
        let file = fileInput.files[0];
        let size = file.size;
        if (size >= 1 * 1024 * 1024) {
            alert('文件大小超出限制');
            info.innerHTML = '文件大小超出限制';
            preview.style.backgroundImage = '';
            return false;
        }
        // 获取File信息:
        info.innerHTML = `文件名称:  + ${file.name}<br>文件大小: ${file.size} <br>上传时间: ${file.lastModifiedDate}`;
        if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
            alert('不是有效的图片文件!');
            preview.style.backgroundImage = '';
            return;
        }
        // 读取文件:
        let reader = new FileReader();
        reader.onload = function(e) {
            let data = e.target.result;
            console.log(preview, 'a标签')
            preview.src = data
        };
        // 以DataURL的形式读取文件:
        reader.readAsDataURL(file);

    });
}

function uploadPicture() {
    let fileInput = document.getElementById('file-input');
    let file = fileInput.files[0];
    let rid = document.getElementById('rid_temp').value;

    let formData = new FormData();
    formData.append('picture', file);
    formData.append('rid', rid);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    xhr.onload = function() {
        let response = JSON.parse(xhr.responseText);
        console.log(response.code);
        if (xhr.status === 200) {
            alert('上传成功！\n服务端给出结果是：' + response.result);
        } else {
            alert('上传失败！\n服务端答道：' + response.msg);
        }
    };
    xhr.send(formData);
}
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
</style>