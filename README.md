# CS7IS5-A-SEM202-201920 ADAPTIVE APPLICATIONS

### Team-James-Adaptive-Purchase-Planner

> You're running to the store after work but realize you left your list at home (ugh). Instead of standing in the dairy aisle wondering how much milk you have left, next time use your phone as your personal grocery shopping assistant. APP (Adaptive Purchase Planner) takes out all the work for you, whether you want to share a virtual list with your spouse and even find easy deals. To help you get your grocery shop on, we've rounded up the best list-managing to streamline your next shopping trip.
The application can keep track of products users bought and recommend them to use when they need them, suggest other products that might interest them, so users can find better and cheaper products more easily.
Our objective is to build an application that will track the users' buying habits through explicit data collection and implicit recognition of users' choices in the app to suggest purchases in a timely manner.


> Demo: https://drive.google.com/file/d/10831LwLYQaKu__veePYLC_cGlartAUS2/view

var embed = require("embed-video")

var vimeoUrl = "http://vimeo.com/19339941"
var youtubeUrl = "https://www.youtube.com/watch?v=twE64AuqE9A"
var dailymotionUrl = "https://www.dailymotion.com/video/x20qnej_red-bull-presents-wild-ride-bmx-mtb-dirt_sport"

console.log(embed(vimeoUrl))
console.log(embed(youtubeUrl))
console.log(embed(dailymotionUrl))

var vimeoId = "6964150"
var youtubeId = "9XeNNqeHVDw"
var dailymotionId = "x20qnej"

console.log(embed.vimeo(vimeoId))
console.log(embed.youtube(youtubeId))
console.log(embed.dailymotion(dailymotionId))
