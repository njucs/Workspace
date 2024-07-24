import torch
from torch.utils.data import Dataset, Subset, DataLoader
from sklearn.model_selection import train_test_split

'''
Use Sklearn's train_test_split function to split the dataset into train, validate, and test sets in a 6:2:2 ratio.
Then, put the split datasets into the customized MyDataset class and use DataLoader to load the datasets.
The shuffle parameter in train_loader is set to True, which means that the dataset will be shuffled randomly at each epoch.
'''

'''
An data example:
{
    'img_id': '04008917-9552-57d5-91cc-299073f2f005.jpg', 
    'text': 'Italy Storms Back Into the World Cup, Stunning Australia in Injury Time', 
    'token': ['Italy', 'Storms', 'Back', 'Into', 'the', 'World', 'Cup', ',', 'Stunning', 'Australia', 'in', 'Injury', 'Time'], 
    'h': {'name': ['World', 'Cup'], 'pos': [5, 7]}, 
    't': {'name': 'barbara bonansea', 'pos': ('0.439167', '0.130326', '0.075', '0.185464')}, 
    'relation': '/per/misc/present_in'
}
'''
# 自定义数据集类
class MyDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __getitem__(self, idx):
        return self.data[idx]

    def __len__(self):
        return len(self.data)

# 读取数据集
data = ... # 数据集

# 划分数据集
train_data, test_data = train_test_split(data, test_size=0.2, random_state=123)
train_data, val_data = train_test_split(train_data, test_size=0.25, random_state=123)

# 定义数据集和数据加载器
train_dataset = MyDataset(train_data)
val_dataset = MyDataset(val_data)
test_dataset = MyDataset(test_data)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)
test_loader = DataLoader(test_dataset, batch_size=32)

