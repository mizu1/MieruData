        //展开聊天框
        document.getElementById('chat-icon').addEventListener('click', function(event) {
            //路径填入
            if(document.getElementById("full_path").textContent == ""){
                alert("请先选择要处理的文件");
                return;
            }
            //展开
            document.getElementById('chat-icon').style.display = 'none';
            document.getElementById('chat-box').style.display = 'block';
            event.stopPropagation();  // 阻止事件冒泡
        });
        //隐藏聊天框
        document.addEventListener('click', function(event) {
            var chatBox = document.getElementById('chat-box');
            var chatIcon = document.getElementById('chat-icon');
        
            if (!chatBox.contains(event.target) && event.target != chatIcon) {
                chatBox.style.display = 'none';
                chatIcon.style.display = 'block';
            }
        });
        // 发送信息
        $('#send-button').click(function() {
            var message = $('#chat-input').val();
            $('#chat-input').val('');
        
            // 添加用户的消息到聊天框
            $('#chat-messages').append(`
                <div class="message message-user">
                    <img src="../static/img/红莉栖.jpg" alt="User Avatar" />
                    <div class="message-content">${message}</div>
                </div>
            `);
        
            // 显示加载指示器
            $('#loading').show();
        
            // 使用 AJAX 发送消息到服务器
            $.post('/chat', { message: message }, function(data) {
                // 隐藏加载指示器
                $('#loading').hide();

                // 创建一个新的消息元素
                var messageElem = $(`
                    <div class="message message-bot">
                        <img src="../static/img/monika.png" alt="Bot Avatar" />
                        <div class="message-content"></div>
                    </div>
                `);

                // 添加新的消息元素到聊天框
                $('#chat-messages').append(messageElem);

                // 逐字显示响应
                var i = 0;
                function typeMessage() {
                    if (i < data.response.length) {
                        messageElem.find('.message-content').append(data.response.charAt(i));
                        i++;
                        setTimeout(typeMessage, 50);  // 100ms 的延迟
                    }
                }
                typeMessage();

                // 如果 show_image 为 true，则显示图片
                if (data.show_image) {
                    $('#myImg').html('<img src="/static/img/createdImg/created.png" width="600px" height="400px"/>');
                }
            });

        });