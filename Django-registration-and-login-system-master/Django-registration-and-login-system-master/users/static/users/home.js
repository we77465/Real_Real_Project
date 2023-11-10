document.addEventListener("DOMContentLoaded", function() {
    const downloadButtons = document.querySelectorAll(".download-button");

    downloadButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            const imageUrl = button.getAttribute("data-url");
            const imageId = button.getAttribute("data-image-id");

            // 显示加载画面
            showLoadingScreen();

            // 发送HTTP请求到Django视图，并将image_id传递过去
            fetch(`/download-image/${imageId}/`)
                .then(response => {
                    if (response.ok) {
                        return response.blob();
                    }
                    throw new Error('error');
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'image.jpg';
                    a.click();
                    window.URL.revokeObjectURL(url);

                    // 隐藏加载画面
                    hideLoadingScreen();
                })
                .catch(error => {
                    console.error(error);

                    // 隐藏加载画面（即使出现错误）
                    hideLoadingScreen();
                });
        });
    });

    function showLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        console.log("123123")
        loadingScreen.style.display = 'flex';
}

    function hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        loadingScreen.style.display = 'none';
}
});




function confirmDelete(button) {
    const imageId = button.getAttribute("data-image-id");
    if (confirm("確定刪除?")) {
        deleteImage(imageId, button);
    }
    event.preventDefault(); // 阻止默認事件
}

function deleteImage(imageId, button) {
    fetch(`/delete-image/${imageId}/`)
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('刪除失敗');
        })
        .then(data => {
            alert(data.message); 
        })
        .catch(error => {
            console.error(error);
        });
}


