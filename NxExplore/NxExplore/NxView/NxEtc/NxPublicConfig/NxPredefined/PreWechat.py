#!/usr/bin/python



corpId = 'wx8b52ff182a74eed5'
secret = 'F5GcJMf6vkDplsUFeSYXi59ui7rhpSqRfUIF_B0VyWqIxVzt1RPbpxYvvJ2e7fy1'


agentIdDict = {
    'default':0,
    'Automation':1,
    'QAinfo':2,
    'xiaoniuniu':3
}

departmentDict={
    'FortiADC':1,
    'QA':2,
    'Dev':3,
    'Product':4
}


qaUserList = [
    'haichaozhang',
    'huimingliu',
    'huzhongling',
    'jiashengzhang',
    'jinzhang',
    'liliwang',
    'rongjinyang',
    'xiangfan',
    'youjunsong',
    'yuyinghan',
    'bofei'

]
devUserList = [
    'jianfengwu'

]
productUserList = [
    'dongmeigong',
    'shijili'

]

otherUserList = [
    'xiaoniuniu'
]


entireUserList = qaUserList+devUserList+devUserList+otherUserList
