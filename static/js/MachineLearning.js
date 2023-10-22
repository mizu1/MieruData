        //对机器学习模型的点击事件进行监听
        document.getElementById("decision-tree-classification").addEventListener("click", function() {
            //先判断路径是否为空，若为空则弹出提示框
            if(document.getElementById("full_path").textContent == ""){
                alert("请先选择要处理的文件");
                return;
            }
            // 传到后端
            document.getElementById("form-container").style.display = "block";
            document.getElementById("tree-form").action = "/tree";
        });
        
        document.getElementById("logistic-regression-classification").addEventListener("click", function() {
            if(document.getElementById("full_path").textContent == ""){
                alert("请先选择要处理的文件");
                return;
            }
            // 传到后端
            document.getElementById("form-container").style.display = "block";
            document.getElementById("tree-form").action = "/logistic";
        });
        
        document.getElementById("svm-classification").addEventListener("click", function() {
            if(document.getElementById("full_path").textContent == ""){
                alert("请先选择要处理的文件");
                return;
            }
            // 传到后端
            document.getElementById("form-container").style.display = "block";
            document.getElementById("tree-form").action = "/svm";
        });
        
        document.getElementById("decision-tree-regression").addEventListener("click", function() {
            if(document.getElementById("full_path").textContent == ""){
                alert("请先选择要处理的文件");
                return;
            }
            // 传到后端
            document.getElementById("form-container").style.display = "block";
            document.getElementById("tree-form").action = "/tree-regression";
        });