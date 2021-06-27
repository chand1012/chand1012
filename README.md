# About Me
My name is Chandler, and I like to code. Ever since I was 8 or 9, I was fascinated by computers and coding. My first venture into coding was a Lego Mindstorms robot. It was graphical, but it was an algorithm of sorts. My first "real" coding was in Ruby, which while I can still code in, was quickly replaced by Python. Since then, Python has been my go-to for most of my projects and for any sort of quick prototypes I want to develop. I also have used C/C++ and NodeJS, the HTML5 Stack, and wrote a Discord bot in Golang. For most of 2019 and the first month of 2020, I worked as a Software Engineering Intern at a division of SealedAir in Northeast Ohio, and it solidified my dream of coding as a full-time job, as well as teaching me a lot about both the field and working for a real company. Currently I am working on [Pillar](https://github.com/pillargg) part time while finishing my Computer Science degree at The University of Akron.

# Questions? Just ask!
I recently started a GitHub Discussions page on my GitHub README. Ask my about past experience, my IDE preferences, my opinion on various programming languages (Spoiler: Python is my favorite!) or anything else you'd like. Find it [here](https://github.com/chand1012/chand1012/discussions)!

# My Big Projects
I started the [WinGuake](https://github.com/chand1012/WinGuake) project, which is supposed to be a port of the Guake Linux terminal for Windows (I haven't been developing on it as much recently due to time constraints, but help would be appreciated and would go toward development!). Recently I have been working heavily on two projects, one that I will release open source in time, and one that has been used by over 100,000 unique users on Discord, that being [Discord-Quick-Meme](https://github.com/chand1012/Discord-Quick-Meme). 

My other hobby is 3D printing, which you can find all of my designs for [here](https://www.thingiverse.com/chand1012/about). I will also be publishing the STEP files to GitHub in the near future.

Finally, I like to write occasionally on [my blog](https://chand1012.dev/). This blog is about any of my projects I think I should write about, random tutorials I feel like writing, and any other random tech topic I want to write about. For your support, I'll put your name on my [Sponsors Page](https://chand1012.dev/sponsors/)!

# Social
[<img height=48 width=48 src="https://camo.githubusercontent.com/68ff38b86f01b428567dcc406116e23728245f4e/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f696e7374616772616d2e737667"/>](https://instagram.com/chand1012)
[<img height=48 width=48 src="https://camo.githubusercontent.com/5db862b15e660451b524382c77f60cbd49f176f9/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f6465765f746f2e737667"/>](https://dev.to/chand1012)
[<img height=48 width=48 src="https://camo.githubusercontent.com/9bbddae7e626bda73c943e06b4568a7a02e193b4/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f747769747465722e737667"/>](https://twitter.com/Chand1012Dev)
[<img height=48 width=48 src="https://camo.githubusercontent.com/2ed658492cb094825d26b06c1275a7e0414f32e4/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f7265646469742e737667"/>](https://www.reddit.com/user/chand1012)
[<img height=48 width=48 src="https://camo.githubusercontent.com/8c6d1bbc6c237b1349a387f8085013d873e173cb/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f737465616d2e737667"/>](https://steamcommunity.com/id/chand1012)
[<img height=48 width=48 src="https://camo.githubusercontent.com/c5942c39052ad962364ea8286a6991f7a9b036bf1d96d20db346d9dfd844dfa4/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f7477697463682e737667"/>](https://twitch.tv/chand1012)

Icons by [edent](https://github.com/edent/SuperTinyIcons).

# GitHub Stats

[![chand1012's github stats](https://github.com/chand1012/chand1012/raw/master/github-metrics.svg)](https://github.com/lowlighter/metrics)

# Blog Posts
--------------------------------

<article class="post">
<h1>Why you should avoid long running recursion in Node.</h1>
<div class="entry">
<p>I don't like recursion. I know its a controversial opinion, but I don't like it. I've had too many issues with recursive functions, plus my brain never really got the concept when I first started programming. I avoid using recursion whenever I can, only using in the most obvious of cases (like the classic factorial example).</p>
<p>Not long ago, I was working on a project for work when I noticed that there were tons of errors in the logs, as the lambda that was running the code kept on running out of memory. The code was in production, and as a temporary fix the RAM for the lambda was cranked from 1GB to 3GB, which would also aid in finding where the bug was coming from. This script was written in NodeJS 14, made to run on a lambda, and acted as a download script. The data being downloaded was gotten from an API that could only return chunks of data, but we needed the whole dataset to run our algorithms on. Our solution was to get the data as a JSON array, then save it to AWS S3, using it as a sort of database for the JSON files. I noticed that to download 100MB of data, the RAM use was well over 1.5GB. While you're almost never going to get a 1:1 data size to memory use ratio, it <strong>should not</strong> be as extreme as that.</p>
<p><img alt="High Memory Use" src="https://raw.githubusercontent.com/chand1012/chand1012.github.io/master/images/lambdaMemoryUseNode.jpg"/></p>
<p>The shown example is quite extreme, as most of the time the data we're downloading doesn't go above 20MB, but there are edge cases were we could be downloading as much as 200MB. If the latter is the case, there's no way going to run as intended.</p>
<p>I did some searching, and I found <a href="https://stackoverflow.com/a/16928870/5178731">this</a> StackOverflow post. It seems that Node's garbage collector doesn't clean up until after recursion is complete, and the recursion in this script did not end until <em>after the main purpose of the script had finished</em>. Here is the original recursive function code:</p>
<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code>
<span class="kd">const</span> <span class="nx">allMessages</span> <span class="o">=</span> <span class="p">[];</span>

<span class="kd">const</span> <span class="nx">objectId</span> <span class="o">=</span> <span class="dl">"</span><span class="s2">someObjectId</span><span class="dl">"</span><span class="p">;</span>

<span class="kd">const</span> <span class="nx">callAPI</span> <span class="o">=</span> <span class="k">async</span> <span class="p">(</span><span class="nx">cursor</span> <span class="o">=</span> <span class="kc">null</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
    <span class="kd">const</span> <span class="nx">headers</span> <span class="o">=</span> <span class="p">{</span><span class="dl">'</span><span class="s1">X-Api-Key</span><span class="dl">'</span><span class="p">:</span> <span class="dl">'</span><span class="s1">someApiKey</span><span class="dl">'</span><span class="p">};</span>
    <span class="kd">const</span> <span class="nx">url</span> <span class="o">=</span> <span class="s2">`https://api.url.here/</span><span class="p">${</span><span class="nx">objectId</span><span class="p">}</span><span class="s2">/</span><span class="p">${</span>
        <span class="nx">cursor</span> <span class="p">?</span> <span class="s2">`?cursor=</span><span class="p">${</span><span class="nx">cursor</span><span class="p">}</span><span class="s2">`</span> <span class="p">:</span> <span class="dl">''</span>
    <span class="p">}</span><span class="s2">`</span><span class="p">;</span>
    <span class="kd">const</span> <span class="nx">resp</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">fetch</span><span class="p">(</span><span class="nx">url</span><span class="p">,</span> <span class="p">{</span> <span class="nx">headers</span> <span class="p">});</span>
    <span class="kd">const</span> <span class="p">{</span> <span class="nx">_next</span><span class="p">,</span> <span class="nx">comments</span> <span class="p">}</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">resp</span><span class="p">.</span><span class="nx">json</span><span class="p">();</span>
    <span class="nx">allMessages</span><span class="p">.</span><span class="nx">push</span><span class="p">(...</span><span class="nx">comments</span><span class="p">);</span>

    <span class="k">if</span> <span class="p">(</span><span class="nx">_next</span><span class="p">)</span> <span class="p">{</span>
        <span class="k">await</span> <span class="nx">callAPI</span><span class="p">(</span><span class="nx">_next</span><span class="p">);</span>
    <span class="p">}</span>
<span class="p">};</span>

<span class="k">await</span> <span class="nx">callAPI</span><span class="p">();</span>

</code></pre></div></div>
<p>The basic idea is that this API returned us a cursor to to paginate the JSON data we were retrieving and storing for later in S3. If the cursor returned null from the API, we knew this was the last page of data and we could break recursion. The solution to this issue was really simple.</p>
<div class="language-javascript highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kd">const</span> <span class="nx">allMessages</span> <span class="o">=</span> <span class="p">[];</span>
<span class="kd">const</span> <span class="nx">objectId</span> <span class="o">=</span> <span class="dl">"</span><span class="s2">someObjectId</span><span class="dl">"</span><span class="p">;</span>

<span class="kd">const</span> <span class="nx">callAPI</span> <span class="o">=</span> <span class="k">async</span> <span class="p">(</span><span class="nx">cursor</span> <span class="o">=</span> <span class="kc">null</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="p">{</span>
    <span class="kd">const</span> <span class="nx">headers</span> <span class="o">=</span> <span class="p">{</span><span class="dl">'</span><span class="s1">X-Api-Key</span><span class="dl">'</span><span class="p">:</span> <span class="dl">'</span><span class="s1">someApiKey</span><span class="dl">'</span><span class="p">};</span>
    <span class="kd">const</span> <span class="nx">url</span> <span class="o">=</span> <span class="s2">`https://api.url.here/</span><span class="p">${</span><span class="nx">objectId</span><span class="p">}</span><span class="s2">/</span><span class="p">${</span>
        <span class="nx">cursor</span> <span class="p">?</span> <span class="s2">`?cursor=</span><span class="p">${</span><span class="nx">cursor</span><span class="p">}</span><span class="s2">`</span> <span class="p">:</span> <span class="dl">''</span>
    <span class="p">}</span><span class="s2">`</span><span class="p">;</span>
    <span class="kd">const</span> <span class="nx">resp</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">fetch</span><span class="p">(</span><span class="nx">url</span><span class="p">,</span> <span class="p">{</span> <span class="nx">headers</span> <span class="p">});</span>
    <span class="kd">const</span> <span class="p">{</span> <span class="nx">_next</span><span class="p">,</span> <span class="nx">comments</span> <span class="p">}</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">resp</span><span class="p">.</span><span class="nx">json</span><span class="p">();</span>
    <span class="nx">allMessages</span><span class="p">.</span><span class="nx">push</span><span class="p">(...</span><span class="nx">comments</span><span class="p">);</span>

    <span class="k">return</span> <span class="nx">_next</span><span class="p">;</span>
<span class="p">};</span>

<span class="kd">var</span> <span class="nx">cursor</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">callAPI</span><span class="p">();</span>

<span class="k">while</span> <span class="p">(</span><span class="nx">cursor</span><span class="p">)</span> <span class="p">{</span>
    <span class="nx">cursor</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">callAPI</span><span class="p">(</span><span class="nx">cursor</span><span class="p">);</span>
<span class="p">}</span>
</code></pre></div></div>
<p>This achieves the exact same functionality while fixing the garbage collector problem of before. Rather than recursively executing, the function is called once before starting a <code class="language-plaintext highlighter-rouge">while</code> loop, which conditionally runs provided that <code class="language-plaintext highlighter-rouge">cursor</code> is not <code class="language-plaintext highlighter-rouge">null</code>, appending the data like before into <code class="language-plaintext highlighter-rouge">allMessages</code>.</p>
<p>This is not the main reason I avoided recursive functions, but it has definitely been added to the list. I (as well as the man who wrote this code) are definitely more wary about using recursive functions on lots of data or long running processes, as you should be as well.</p>
</div>
<a class="read-more" href="https://chand1012.dev/NodeRecursionBad/">Read More</a>
</article>
<article class="post">
<h1>Python For Programmers Part 3</h1>
<div class="entry">
<p>This is a series on Python and how to correctly use Python when coming from a background in another computer language. Because of this, this will not be a slow intro into programming and it will be assumed you have a preferred text editor and are smart enough to get Python running. You can download installers and packages from their official website found <a href="https://www.python.org/downloads/">here</a>. Basic knowledge of how to use <a href="https://git-scm.com/">Git</a> and how to operate a computer is also preferred.</p>
</div>
<a class="read-more" href="https://chand1012.dev/PythonForProgrammers3/">Read More</a>
</article>
<article class="post">
<h1>How to Install Node on Linux the Easy Way.</h1>
<div class="entry">
<p>I recently started working on a few major NodeJS project, and found that installing the latest LTS release could be rather cumbersome on Linux. The application we're developing is being hosted on Heroku, and will not be using a Docker container, and for a few reasons we would rather develop locally rather than in a container. Here is how I installed NodeJS and NPM on my Linux installations, and I found it quite easy. While this tutorial will be using Ubuntu's <code class="language-plaintext highlighter-rouge">apt</code> and Arch Linux's <code class="language-plaintext highlighter-rouge">pacman</code>, the process should be similar for most distributions. See <a href="https://nodejs.org/en/download/package-manager/">here</a> for more information about installing NodeJS and NPM via your package manager.</p>
</div>
<a class="read-more" href="https://chand1012.dev/NodeTheEasyWay/">Read More</a>
</article>
<article class="post">
<h1>Why I hate being a developer around Christmas time.</h1>
<div class="entry">
<p>Christmas time is a time of joy, family, giving, and life. Unless its 2020.</p>
</div>
<a class="read-more" href="https://chand1012.dev/ChristmasTimeRant/">Read More</a>
</article>
<article class="post">
<h1>Fixing Commit Messages. Git Gud. Advanced-ish Git Part 2.</h1>
<div class="entry">
<h1 id="intro">Intro</h1>
</div>
<a class="read-more" href="https://chand1012.dev/git-gut2/">Read More</a>
</article>



--------------------------------

# Conclusion

More posts can be found on the [blog](https://chand1012.dev/) or on [dev.to](https://dev.to/chand1012). Hope you find my projects useful!

# Script Details

Update script written in Python.

This script was last updated at 06/27/2021, 00:56:30 UTC.

<img height=48 width=48 src="https://camo.githubusercontent.com/cc1b5b07ad8a80491b42035775baedf76a3b836c/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f707974686f6e2e737667"/>
