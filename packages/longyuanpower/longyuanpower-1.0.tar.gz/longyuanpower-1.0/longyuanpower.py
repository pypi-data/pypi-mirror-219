import requests

"""
欢迎使用龙源power
简要介绍一下参数
api_base_url:是固定的api接口:http://172.24.187.133:5446/longyuanapi
api_key:是发放给您的一个独有的密钥
show:True->保存图片 False->不保存图片
output:True->保存预测结果文件 False->不保存预测结果文件
train:True->使用您的数据集进行训练并预测False->使用我们现有的模型进行预测
"""


class longyuanapi:
    def __init__(self, api_base_url, api_key, show, output, train):
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.show = str(show)
        self.output = str(output)
        self.train = str(train)

    def savepredictfile(self, csv_file):
        # """
        # csv_file是您要进行预测的文件的地址
        # """
        url = self.api_base_url
        # 增加身份验证头部
        headers = {
            'Authorization': self.api_key,
            'show': self.show,
            'output': self.output,
            'train': self.train,
        }
        files = {'file': open(csv_file, 'rb')}
        response = requests.post(url, files=files, headers=headers)
        if response.status_code == 200:
            if self.output == 'True' and self.show == 'False':
                with open('predictions.csv', 'wb') as file:
                    file.write(response.content)
            elif self.output == 'False' and self.show == 'True':
                with open('res_picture.png', 'wb') as file:
                    file.write(response.content)
            else:
                with open('res.zip', 'wb') as file:
                    file.write(response.content)
