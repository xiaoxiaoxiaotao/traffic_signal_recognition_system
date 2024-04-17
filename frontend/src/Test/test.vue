<template>



    <el-upload
    class="upload-demo"
    action="https://jsonplaceholder.typicode.com/posts/"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :file-list="fileList"
    list-type="picture">
    <el-button size="large" type="primary">Please click here to upload the picture</el-button>
    <div slot="tip" class="el-upload__tip">only the jpg/png files，no more than 500kb</div>
    </el-upload>


</template>







<script>
     export default {
    data() {
      return {
        
        fileList: [{name: 'food.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}, {name: 'food2.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}],
    
        
    };
    },

    methods: {
      handleRemove(file, fileList) {
        console.log(file, fileList);},
      handlePreview(file) {
        console.log(file);},

     
    }
  }
</script>