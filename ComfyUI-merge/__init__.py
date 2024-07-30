import torch
import typing as t
from typing import Tuple, List

class Merge:
    CATEGORY = "ASVL"
    
    # 定义允许的方向选项
    DIRECT_OPTIONS = ["horizontal", "vertical"]
    
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, t.Union[t.Any, List[t.Any]]]:
        return {
            "required": {
                "image_one": ("IMAGE",),
                "image_two": ("IMAGE",),
            },
            "optional": {
                "direction": ("STRING", "horizontal")  # 可选参数，带默认值
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("merged_image",)
    FUNCTION = "execute"  # 方法名

    @classmethod
    def execute(cls, image_one: torch.Tensor, image_two: torch.Tensor, direction: str = "horizontal") -> Tuple[torch.Tensor]:
        # 确保所有图像的尺寸一致
        if image_one.shape != image_two.shape:
            raise ValueError("Both images must have the same dimensions")

        # 确保方向参数是有效的
        if direction not in cls.DIRECT_OPTIONS:
            raise ValueError(f"Direction must be one of {cls.DIRECT_OPTIONS}")

        # 根据方向合并图像张量
        combined_image = torch.cat((image_one, image_two), 1 if direction == "vertical" else 2)

        return (combined_image,)

    @classmethod
    def select_direction(cls) -> str:
        # 这里模拟用户选择方向的过程
        # 实际应用中，这里可能是一个下拉菜单或其他UI组件
        print("Please select the merge direction from the options:")
        for index, option in enumerate(cls.DIRECT_OPTIONS, start=1):
            print(f"{index}. {option}")
        
        # 模拟用户输入，这里使用硬编码的值来示例
        # 实际应用中，这里应该是用户输入的获取
        user_input = input("Enter your choice (number): ")
        try:
            selected_index = int(user_input) - 1
            selected_direction = cls.DIRECT_OPTIONS[selected_index]
        except (IndexError, ValueError):
            print("Invalid selection, using default direction 'horizontal'.")
            selected_direction = "horizontal"
        
        return selected_direction

# 确保NODE_CLASS_MAPPINGS映射的是类本身
NODE_CLASS_MAPPINGS = {
    "ASVL": Merge,
}

# 模块导出
__all__ = ['NODE_CLASS_MAPPINGS']

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "ASVL": "Merge—horizontal_vertical",
}

# 模拟节点执行过程
if __name__ == "__main__":
    # 创建图像数据，实际应用中这些数据可能来自图像文件或其他源
    image_one = torch.randn(3, 100, 100)
    image_two = torch.randn(3, 100, 100)
    
    # 选择合并方向
    direction = Merge.select_direction()
    
    # 执行合并操作
    try:
        merged_image, = Merge.execute(image_one, image_two, direction)
        print(f"Merge successful. Merged image shape: {merged_image.shape}")
    except ValueError as e:
        print(f"Error during merge: {e}")