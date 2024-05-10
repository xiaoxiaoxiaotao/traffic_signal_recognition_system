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
            fileInput.value = null; // 清除选中的文件
            return false;
        }
        // 获取File信息:
        info.innerHTML = `文件名称:  + ${file.name}<br>文件大小: ${file.size} <br>上传时间: ${file.lastModifiedDate}`;
        if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
            alert('不是有效的图片文件!');
            preview.style.backgroundImage = '';
            fileInput.value = null; // 清除选中的文件
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