# smallTetris
## 注意，這是使用現成的俄羅斯方塊改出來的 [來源](https://vocus.cc/article/627f79b3fd8978000128e797)  
### 螢幕截圖
![image](https://github.com/PaidaAn/smallTetris/blob/main/images/screenshot.png)
我改的部分有:  
+ 新增雙人模式
+ 可以連接至arduino
+ 雙人模式的互動機制
+ HOLD方塊
## TetrisMain
此為遊戲主程式，包含了流程、所有與pygame和arduino相關的程式。
## TetrisClass
此為將參考資料改寫成class，遊戲的主要邏輯包含在此。
## 俄羅斯方塊主要邏輯
### 儲存方式
將方塊的所有狀態以陣列的方式儲存，這裡的方式是將背景用二維陣列(10\*20)儲存，以0代表空方塊。  
而玩家可操控的掉落方塊以二維陣列(4\*4)陣列儲存，並且會隨著時間或玩家操控而在背景陣列上移動位置。  
可操控方塊的形狀使用一維陣列表示，每個數字代表此圖案的一格方塊以由上而下、由左而右放進可操控方塊陣列裡，例如L型方塊用(4,8,12,13)表示。
### 可操控方塊與背景互動
在判斷可操控方塊能不能往左、右、下走及旋轉時，會利用可操控方塊在背景陣列上的位置，配合方塊形狀將方塊投影到背景陣列上，以此來達成方塊與背景互動。  
在判斷可操控方塊觸底時，也是利用上述原理將可操控方塊儲存至背景陣列，然後可操控方塊將回到遊戲頂部進行另一個方塊下墜。
