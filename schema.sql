drop database if exists awesome;

create database awesome;

use awesome;

grant select, insert, update, delete on awesome.* to 'www-data'@'localhost' identified by 'www-data';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
	`rd_times` bigint not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

INSERT INTO `blogs` VALUES ('001474768787516c6e331dcfc764c1890089aa41a1701e1000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','测试','这是摘要','这是内容','1474768844.5539','25'), ('0014760151225506c04dbbc77ec4eeb840b344af806f85f000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','关于server中文件路径的问题','这几天一直在搞这个头像问题，网上搜出来一大堆都是HTML的，给的要么是绝对路径，类似于C:\\xx\\xx.jpg的形式，要么是相对路径，类似于.\\xx.jpg的形式，两种形式放到webserver中都不...','这几天一直在搞这个头像问题，网上搜出来一大堆都是HTML的，给的要么是绝对路径，类似于C:\\xx\\xx.jpg的形式，要么是相对路径，类似于.\\xx.jpg的形式，两种形式放到webserver中都不行。\n\n最后在玩momentum（一款chrome插件）的时候，想看看源代码，突然发现并不应给出相对路径前面那个“.”，直接\\xx,jpg就行了。\n\n这样，头像功能就上线了。\n\n        后面的任务依然不轻，具体还有以下几个方面：\n\n        1. 完善评论、用户两个管理页面。\n\n        2. 完善首页翻页功能。\n\n        3. 完善细节，主要是外观上的细节。\n\n        4. 网站部署上线。\n\n        5. 实现代码高亮。\n\n        6. 实现博客中插入图片的功能。\n\n暂时能想到的就这么多，网站已经做了额大概，接下来就是完善，上线，维护。','1476015122.55052','67'), ('0014762788483545be080fbb09c4d4ba2423d13b7b8acde000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','markdown','#Heading\n\nLorem ipsum dolor sit **amet**, consectetur adipisicing elit, sed do eiusmod tempor incidi...','#Heading\n\nLorem ipsum dolor sit **amet**, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. [This is a link](#)\n\n* Item\n* Item\n* Item\n\n## Heading\n\nUt enim ad *minim* veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n\n<a href=\"#\">This link is written in HTML</a>','1476278848.35446','23'), ('0014763439895071c2beb5afedb4e4cba4198a8a7eb36ae000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','HTML编辑器终于搞定了','费了还几天的功夫，最后原来是[廖老师](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c0...','费了还几天的功夫，最后原来是[廖老师](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)把**uikit.min.js**改了，导致一直找不到UIKit，替换成官方原版的就可以了。也感谢UIKit官方群里面的网友帮助我远程调试。\n\n这个博客已经写了好久了，到现在已经完成了70%吧，还有好多功能不完善。后期还想做的事情有：\n\n1. 实现图片上传\n2. 改善翻页标签\n3. 实现代码高亮\n\n另外，内核这边可以开工了，要学习的东西还有很多，comeon!!!','1476343989.50759','36'), ('0014765253789259e3dc11a55ae44f2b83bd57fe124b2b8000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','测试','测试...','测试','1476525378.92558','18'), ('0014831607268399bcfd293abc1490b8c6d1b9f75b34a95000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','开始学习Javaweb了','开始觉得很容易，后来觉得还是python好，不是因为逻辑复杂，而是因为很多问题，比如中文编码的问题，设置过滤器都不行，好像解决起来也不是那么容易。还有那个IDE，随便设置一下就可以导致争个项目推倒重来...','开始觉得很容易，后来觉得还是python好，不是因为逻辑复杂，而是因为很多问题，比如中文编码的问题，设置过滤器都不行，好像解决起来也不是那么容易。还有那个IDE，随便设置一下就可以导致争个项目推倒重来，可呢个有方法解决，但是对于新手而言，还是太不友好了。\npython相对于Java要简单的多，不需要IDE，也没有那么多中间文件，只要把源文件备份到github上，随时都可以运行。还有在函数参数处理上，Java貌似有点弱，但是代码太过于繁杂。python是一门好编程语言，值得深入学习。','1483160726.83993','7');
INSERT INTO `comments` VALUES ('0014754914570995524e1a1ea594fbebd37af2c2674c335000','0014754022499007520afeb41d4452c9448b345fa8bfce1000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','哈哈','1475491457.10025'), ('00147549149667100a1b668f5144b5bb9face18c62f5782000','0014754022499007520afeb41d4452c9448b345fa8bfce1000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','哈哈哈哈哈哈哈哈','1475491496.67251'), ('00147549161558022fee5a1a6d64497b45fa05bf639987f000','0014754022499007520afeb41d4452c9448b345fa8bfce1000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈','1475491615.58131'), ('0014754932639407c3b5eee4772427cb3b0050a01994fbd000','0014754022499007520afeb41d4452c9448b345fa8bfce1000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','啊哈哈哈','1475493263.94159'), ('001475497718115f7fd5cde937d4ca9b381cedf870657ee000','0014754022499007520afeb41d4452c9448b345fa8bfce1000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','哈哈','1475497718.11636'), ('001475918033951786406d77e2e4a76838f41879892aece000','001475404195841f0568dbf94b54c2691e371259bae9a53000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','cedhi','1475918033.9516'), ('00147592059648522ce85116abb4eb5b540af5bfb7cd786000','001475404195841f0568dbf94b54c2691e371259bae9a53000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','哈哈','1475920596.48517'), ('0014759344691980d99a9c8f4764c46b2d828e8d88d5854000','001475404195841f0568dbf94b54c2691e371259bae9a53000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','测试','1475934469.19837'), ('001475934486455c3d0df24fea540dbbfe0c1fbe31d112c000','001475404195841f0568dbf94b54c2691e371259bae9a53000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','这篇文章很赞','1475934486.45535'), ('001476056917963dc65a6dae8814bd8bf9594283ac1bc1a000','0014760151225506c04dbbc77ec4eeb840b344af806f85f000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','这篇文章很赞','1476056917.96359'), ('00147609251802670ae754187f34854bcccbc4200094f29000','001476060780356fd5f705d10ef4d6ebee7a9b97d220a15000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','效果不错','1476092518.02603'), ('0014761021473827e61205079814451961e31a3687ee4e2000','00147489864760275fbd94374c14eaa9c1b254a9522ca4c000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','不错，受教了哈哈','1476102147.38228'), ('0014761633098961068a3e653234e28a5f870e01a4f70f1000','001474768787516c6e331dcfc764c1890089aa41a1701e1000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','测试评论数显示功能','1476163309.89662'), ('001476163325732e3133024b8454be5adccf10229b1b2cf000','0014760151225506c04dbbc77ec4eeb840b344af806f85f000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','测试评论数显示功能','1476163325.73252'), ('0014762790585888ce3c9fff6fb4a15a8c2c6b71b1358e0000','0014762788483545be080fbb09c4d4ba2423d13b7b8acde000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','本身支持markdown，但是缺一个markdown编辑器','1476279058.58948'), ('001476502829379d4e0233cb8a5468ea2d259462618e79c000','0014763439895071c2beb5afedb4e4cba4198a8a7eb36ae000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','还是有问题的，HTML编辑器的内容不能保存，也就是添加htmledictor后v-model这个双向绑定的属性失效了，待修复','1476502829.37931'), ('00147955734297763098dd414d54d32a0916e8db978cef8000','0014763439895071c2beb5afedb4e4cba4198a8a7eb36ae000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','啊啊啊啊啊啊啊','1479557342.97732'), ('0014831097697766096b2da2ad84703aafca3421728c190000','0014765253789259e3dc11a55ae44f2b83bd57fe124b2b8000','00147469895059572af5731b8314137b744cab44ffd5045000','周翔','/static/img/zx.png','javaweb 好麻烦，还是python好','1483109769.77617');
INSERT INTO `users` VALUES ('00147469895059572af5731b8314137b744cab44ffd5045000','1160296050@qq.com','a0262ae2e6248cf80f366dda59b4739ded652bd4','1','周翔','/static/img/zx.png','1474698950.59681'), ('001474714533322e80f0f95361f4647b46ce31f79e120eb000','1484033364@qq.com','e54f3627493066c2ac0641979a1d20e6cb2ac915','0','wcp','http://www.gravater.com/avater/7b44fd7e3989237f3f07ada7ac9d2f7c?d=mm&s=120','1474714533.32209');
