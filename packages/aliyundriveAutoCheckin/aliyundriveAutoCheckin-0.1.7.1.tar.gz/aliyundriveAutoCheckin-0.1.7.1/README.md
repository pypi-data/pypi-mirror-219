# 阿里云盘自动签到(aliyundriveAutoCheckin)

1. `refresh_token`: 阿里云盘的refresh_token，用于获取access_token。
2. `is_get_reward`: 是否领取签到奖励。如果值为 "是"，则在签到后会尝试领取奖励。
3. `is_send_email`: 是否发送签到结果的邮件。如果值为 "是"，则会尝试发送邮件。
4. `is_custom_email`: 是否使用自定义的SMTP服务器发送邮件。如果值为 "是"，则会使用接下来的字段作为SMTP服务器的配置。
5. `to_addr`: 邮件的接收者地址。

如果 `is_custom_email` 为 "是"，则还需要提供以下字段：

1. `smtp_server`: SMTP服务器的地址。
2. `smtp_port`: SMTP服务器的端口。
3. `smtp_user`: SMTP服务器的用户名。
4. `smtp_password`: SMTP服务器的密码。

# refresh_token获取方法:

![2](https://xiaohan17.oss-cn-hangzhou.aliyuncs.com/xiaohan17/wenzhang/202307141529209.png)

![3](https://xiaohan17.oss-cn-hangzhou.aliyuncs.com/xiaohan17/wenzhang/202307141529614.png)

![4](https://xiaohan17.oss-cn-hangzhou.aliyuncs.com/xiaohan17/wenzhang/202307141529639.png)



# 电脑开机自动阿里云盘签到方法:

在Windows操作系统上，想要实现开机自启动，我们可以通过“启动”文件夹来实现。具体操作步骤如下：

1. 打开运行窗口。可以通过按下Win+R快捷键，或者在任务栏的搜索栏输入“运行”打开。

   ![5](https://xiaohan17.oss-cn-hangzhou.aliyuncs.com/xiaohan17/wenzhang/202307141530026.png)

2. 在运行窗口中输入 `shell:startup`，然后按回车键。

3. 这将打开启动文件夹。你只需要将想要在启动时运行的exe文件的快捷方式拖到这个文件夹中就可以了。

4. 如果你的exe文件在桌面上，你可以右键点击它，然后选择“发送到”->“桌面（创建快捷方式）”。然后将这个新创建的快捷方式移动到启动文件夹。

   ![6](https://xiaohan17.oss-cn-hangzhou.aliyuncs.com/xiaohan17/wenzhang/202307141530782.png)

![7](https://xiaohan17.oss-cn-hangzhou.aliyuncs.com/xiaohan17/wenzhang/202307141531419.png)

这样，每次你的电脑启动时，这个exe文件就会自动运行。





