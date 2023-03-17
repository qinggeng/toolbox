import toolbox.subtitles as sts
import pysrt
########################################
#           测试查找句号字幕           #
########################################
srt_txt = """
1
00:00:00,940 --> 00:00:03,140
Welcome back to Control System Lectures.

2
00:00:04,140 --> 00:00:04,540
In this video,

3
00:00:04,590 --> 00:00:12,200
I want to introduce a topic that is sort of a bridge to larger and more useful discussions on system stability.

4
00:00:12,940 --> 00:00:14,070
Before we jump right into them,

5
00:00:14,100 --> 00:00:22,379
I think it's important to set the stage first and describe why we need so many different types of design tools in classical control theory.

6
00:00:23,220 --> 00:00:24,119
And maybe in the process,

7
00:00:24,139 --> 00:00:27,700
we'll answer a few lingering questions you might have about them.

8
00:00:27,760 --> 00:00:30,589
Some of these topics include the Ralph Hurwitz criterion,

9
00:00:30,589 --> 00:00:31,089
Nyquist plots,

10
00:00:32,499 --> 00:00:34,000
Bode plots,

11
00:00:34,330 --> 00:00:35,750
and Root Locus.

12
00:00:36,799 --> 00:00:36,799
Therefore,

13
00:00:37,299 --> 00:00:37,860
in this video,

14
00:00:38,260 --> 00:00:41,230
I'm just going to address really the following question.

15
00:00:41,919 --> 00:00:49,280
How can we determine the stability of a closed loop control system? And by answering that question,

16
00:00:49,280 --> 00:00:56,230
we'll be ready to move on to what are extremely powerful tools in control system design and analysis.

17
00:00:56,360 --> 00:00:57,740
Before we march off and start answering that question directly,

18
00:00:58,000 --> 00:01:03,480
I want to make sure we're all on the same page regarding some terms.

19
00:01:03,720 --> 00:01:03,720
Namely,

20
00:01:04,099 --> 00:01:08,050
some interesting differences between open loop and closed loop control systems.

21
00:01:09,130 --> 00:01:10,180
If you've never heard of these terms,

22
00:01:10,240 --> 00:01:14,059
I recommend that you first check out my video on open loop and closed loop systems.

23
00:01:14,680 --> 00:01:16,160
But if you have a general idea of what they are,

24
00:01:16,639 --> 00:01:19,469
then the next section might provide a little more understanding.

25
00:01:20,479 --> 00:01:21,239
By definition,

26
00:01:21,840 --> 00:01:25,970
open loop control systems do not use feedback to determine if the system has met its desired state.

27
00:01:28,479 --> 00:01:28,479
That is,

28
00:01:28,980 --> 00:01:30,380
they don't observe or sense the output.

29
00:01:31,829 --> 00:01:34,700
A block diagram of an open loop system might look something like this.

30
00:01:38,000 --> 00:01:39,000
The input into the system is the reference signal,

31
00:01:39,119 --> 00:01:39,439
or the commanded state,

32
00:01:39,779 --> 00:01:41,880
and the output is the observed state.

33
00:01:43,279 --> 00:01:43,959
By contrast,

34
00:01:44,000 --> 00:01:47,790
a closed loop system does use feedback of the output state to alter the input.

35
00:01:49,120 --> 00:01:49,120
However,

36
00:01:49,120 --> 00:01:49,880
as you can see,

37
00:01:50,430 --> 00:01:53,759
the original reference signal is now the output of the comparator.

38
00:01:54,820 --> 00:01:59,889
And the new closed loop reference is a completely new signal.

39
00:02:00,239 --> 00:02:07,860
What I find interesting about this is that the difference between open loop and closed loop is dependent on what you label as the reference signal and what is the output.

40
00:02:08,939 --> 00:02:13,809
I could take everything inside of this dashed box and call it the plant.

41
00:02:13,979 --> 00:02:16,860
And now since the reference doesn't depend on the output of this plant,

42
00:02:17,649 --> 00:02:19,339
it can be considered an open loop system again.

43
00:02:21,080 --> 00:02:23,179
Let me give you an example to illustrate what I mean.

44
00:02:24,059 --> 00:02:26,730
So you were given a rock that was sitting on a table,

45
00:02:26,760 --> 00:02:30,239
and you were told to keep that rock exactly at the same spot on the table,

46
00:02:31,040 --> 00:02:32,980
even in the presence of disturbances,

47
00:02:33,260 --> 00:02:37,310
like the table shaking or really high winds.

48
00:02:37,610 --> 00:02:38,360
You want to model the system.

49
00:02:39,040 --> 00:02:40,380
So you start with the transfer function,

50
00:02:40,660 --> 00:02:41,939
where the input is force,

51
00:02:42,379 --> 00:02:45,399
and the output is the position of the rock x.

52
00:02:46,000 --> 00:02:46,000
Now,

53
00:02:46,460 --> 00:02:48,020
you could either look this up in a table,

54
00:02:48,280 --> 00:02:52,269
or you could easily calculate it to be 1 over ms squared.

55
00:02:52,800 --> 00:02:53,780
And you can draw the block diagram like this.

56
00:02:55,740 --> 00:02:58,129
And what this is saying is that if you apply a force to the rock,

57
00:02:58,400 --> 00:02:59,720
it's going to start to move.

58
00:03:00,760 --> 00:03:03,900
And you can see that this transfer function makes sense,

59
00:03:03,920 --> 00:03:04,720
since if you have a force input,

60
00:03:04,800 --> 00:03:07,680
you can divide by mass to get acceleration.

61
00:03:08,700 --> 00:03:10,760
And when you integrate acceleration twice,

62
00:03:10,760 --> 00:03:11,760
you get position.

63
00:03:12,300 --> 00:03:14,839
And since 1 over s is the plus transform of an integral,

64
00:03:15,340 --> 00:03:21,599
that's exactly what the transfer function is doing to transfer the force input into a position output.

65
00:03:22,240 --> 00:03:23,360
And this is an open loop system,

66
00:03:23,640 --> 00:03:31,630
because the amount of force needed to keep the rock exactly at the same spot is not dependent on where the rock is currently located.

67
00:03:33,240 --> 00:03:35,140
If a disturbance force moved the rock,

68
00:03:35,210 --> 00:03:36,020
without knowing where the rock was,

69
00:03:36,060 --> 00:03:40,400
you wouldn't know how much force or in which direction to apply it.

70
00:03:40,440 --> 00:03:41,559
As a side note here,

71
00:03:41,690 --> 00:03:47,239
you could attempt to measure the disturbance force and counter it with an equal and opposite input force.

72
00:03:48,399 --> 00:03:53,820
So the system would still be subjected to disturbances that you don't measure or didn't know about,

73
00:03:53,820 --> 00:03:58,110
and any error in the measurement will ultimately add error to your result.

74
00:03:59,319 --> 00:04:00,399
At this point,

75
00:04:00,479 --> 00:04:01,180
you decide that in order to meet the requirements,

76
00:04:01,199 --> 00:04:06,070
you have to add feedback to adjust the amount of force on the rock based on its position.

77
00:04:06,919 --> 00:04:07,550
To do this,

78
00:04:07,600 --> 00:04:10,199
you attach the rock to one side of a spring.

79
00:04:10,590 --> 00:04:11,290
And on the other side of a spring,

80
00:04:11,339 --> 00:04:12,959
you put a solid wall.

81
00:04:13,520 --> 00:04:19,440
Now the spring produces an additional force that is negatively proportional to its stretched distance.

82
00:04:20,280 --> 00:04:20,960
Or writing this in block diagram form,

83
00:04:21,340 --> 00:04:23,620
we can feedback the distance,

84
00:04:23,930 --> 00:04:26,980
multiply it by spring constant k,

85
00:04:26,980 --> 00:04:29,440
and subtract this force from the reference force.

86
00:04:30,240 --> 00:04:32,919
Now if there's a disturbance on the system,

87
00:04:33,259 --> 00:04:37,300
the feedback path will cause the system to oscillate around the initial starting position.

88
00:04:38,860 --> 00:04:41,200
Feedback is definitely an improvement,

89
00:04:41,520 --> 00:04:43,199
since the rock will always tend to oscillate back towards the reference position.

90
00:04:45,999 --> 00:04:46,959
But it's probably not good enough,

91
00:04:46,959 --> 00:04:48,160
because without any damping,

92
00:04:48,209 --> 00:04:53,259
the rock will continue to oscillate forever and never actually come back to rest at its reference point.

93
00:04:54,199 --> 00:04:54,639
But let's look at this.

94
00:04:55,139 --> 00:04:56,299
We have this closed loop system.

95
00:04:57,199 --> 00:05:01,819
But if we treat the spring and mass together as the entire plant,

96
00:05:01,879 --> 00:05:04,379
we can rewrite the transfer function in this manner.

97
00:05:05,299 --> 00:05:07,489
One divided by ms squared plus k.

98
00:05:08,019 --> 00:05:09,799
And now this looks like an open loop system.

99
00:05:10,440 --> 00:05:10,690
More specifically,

100
00:05:10,690 --> 00:05:14,519
we're treating the feedback path as the plant,

101
00:05:14,519 --> 00:05:16,639
and it's accounted for in the transfer function.

102
00:05:17,539 --> 00:05:17,959
But mathematically,

103
00:05:18,259 --> 00:05:23,239
there's no difference between this transfer function and the system just above it.

104
00:05:23,520 --> 00:05:24,239
Now when you add disturbance,

105
00:05:24,699 --> 00:05:30,509
that internal feedback path is going to cause the rock to oscillate around its reference point.

106
00:05:30,660 --> 00:05:31,779
Now with this transfer function,

107
00:05:31,959 --> 00:05:33,600
we can add another feedback path.

108
00:05:34,859 --> 00:05:37,919
Say a damper to damp the oscillations over time.

109
00:05:38,029 --> 00:05:38,820
And just like we did before,

110
00:05:38,820 --> 00:05:44,580
we can condense this block diagram into another single open loop transfer function.

111
00:05:45,519 --> 00:05:49,119
So you can see when you add feedback control to an open loop system,

112
00:05:49,139 --> 00:05:51,160
you are changing the dynamics of the system,

113
00:05:51,379 --> 00:05:52,919
generally making them more complicated.

114
00:05:54,119 --> 00:05:54,119
However,

115
00:05:54,220 --> 00:05:56,919
once you rewrite the dynamics in the familiar open loop way,

116
00:05:57,680 --> 00:06:02,819
then the same analysis techniques will work for both.

117
00:06:03,339 --> 00:06:05,199
So the question becomes,

118
00:06:05,240 --> 00:06:08,399
how do we determine the stability of this open loop system? And then,

119
00:06:08,479 --> 00:06:11,099
by rewriting a closed loop system,

120
00:06:11,139 --> 00:06:18,820
can we just apply the exact same techniques to both? All transfer functions can be rewritten as the division of two polynomials,

121
00:06:19,039 --> 00:06:20,459
a numerator and a denominator.

122
00:06:21,440 --> 00:06:25,929
We determine stability of an open loop system by looking at the poles of the transfer function,

123
00:06:26,400 --> 00:06:29,649
which are the roots of the characteristic equation.

124
00:06:29,899 --> 00:06:32,859
These roots will have a real component and an imaginary component.

125
00:06:33,709 --> 00:06:33,879
For this example,

126
00:06:33,879 --> 00:06:36,779
this transfer function,

127
00:06:36,799 --> 00:06:37,659
G of S,

128
00:06:37,659 --> 00:06:40,029
has roots at minus 1 and minus 2.

129
00:06:40,359 --> 00:06:45,899
Now you can plot these roots to see them visually or just assess the stability directly.

130
00:06:46,179 --> 00:06:49,199
If all of the roots exist in the left half plane,

131
00:06:49,519 --> 00:06:51,839
that is that they have negative real components,

132
00:06:52,539 --> 00:06:53,919
then the system is stable.

133
00:06:54,539 --> 00:06:59,299
This is easy to prove using the inverse Laplace transform of G of S.

134
00:06:59,309 --> 00:07:03,679
You can simplify the transfer function using partial fraction expansion.

135
00:07:05,820 --> 00:07:07,950
And what you'll be left with is a summation of poles with various gains,

136
00:07:08,000 --> 00:07:10,369
A and B in this case.

137
00:07:13,279 --> 00:07:16,279
Now taking the inverse Laplace is the gain of the numerator times E to the S T.

138
00:07:16,750 --> 00:07:23,119
And if each S or each root is negative,

139
00:07:23,179 --> 00:07:25,680
then the response will decay exponentially as time increases,

140
00:07:25,800 --> 00:07:28,000
which is a stable system.

141
00:07:29,889 --> 00:07:32,529
So that's how we determine stability of an open loop system.

142
00:07:33,699 --> 00:07:34,379
Your next question might be,

143
00:07:34,399 --> 00:07:44,360
how is that any different than what we would do for a closed loop system? So your first guess for determining the stability of a closed loop system might be 1,

144
00:07:44,380 --> 00:07:47,699
rewrite the system as an open loop transfer function.

145
00:07:48,879 --> 00:07:52,639
That is basically reduce the block diagram into a single transfer function.

146
00:07:53,160 --> 00:07:53,160
2,

147
00:07:53,440 --> 00:07:56,439
solve for the roots of the characteristic equation.

148
00:07:57,459 --> 00:08:03,379
And then the third step would be to look at the real component of those roots and determine whether the system is stable or not.

149
00:08:03,959 --> 00:08:04,209
That seems easy enough,

150
00:08:04,219 --> 00:08:07,359
right? Well let's try it in practice.

151
00:08:11,009 --> 00:08:12,469
Let's take an open loop system that has two separate processes,

152
00:08:12,549 --> 00:08:16,609
a control process H and a plant G.

153
00:08:16,639 --> 00:08:18,859
And this is an open loop system,

154
00:08:18,889 --> 00:08:25,619
and so we know that we can determine stability by looking at the poles of the combined transfer function H times G.

155
00:08:26,629 --> 00:08:29,660
But what if we close the loop,

156
00:08:29,760 --> 00:08:34,540
we can rewrite the transfer function as H times G divided by 1 plus H times G.

157
00:08:34,559 --> 00:08:37,230
And this is a closed loop system.

158
00:08:39,119 --> 00:08:41,410
But stability is still found by looking at the open loop representation.

159
00:08:42,039 --> 00:08:46,910
So in this case it's by finding the roots of 1 plus H G.

160
00:08:46,949 --> 00:08:52,559
So it looks like all you have to do is add 1 to the open loop transfer function and then solve for the roots.

161
00:08:53,480 --> 00:08:53,480
Great.

162
00:08:54,059 --> 00:09:05,109
So why don't we do this all the time? Where are we bothering to use tools like Bode plots or Ralph Herwood's Criterion or Nyquist plots or the root locus method? Well the answer has two parts.

163
00:09:06,720 --> 00:09:12,409
The first part is that with the advent of computers and software packages like MATLAB solving for these roots are no problem.

164
00:09:12,440 --> 00:09:16,070
However historically solving for these roots was a huge problem.

165
00:09:16,519 --> 00:09:21,160
Try solving for the roots of an 8th order polynomial and see how easy it is without a computer.

166
00:09:21,819 --> 00:09:32,569
So we were able to determine the roots of G times H though because both the controller and the system dynamics are built up with poles and zeros such that the roots are easy to see.

167
00:09:34,699 --> 00:09:39,719
This usually falls out that way because of the way that the dynamics are modeled and because the control system is chosen by the engineer.

168
00:09:40,759 --> 00:09:46,439
You can see very easily in this example that the roots are at minus 1 minus 3 minus 4 and 0.

169
00:09:46,520 --> 00:09:48,539
And you know that this is a stable system.

170
00:09:49,639 --> 00:09:50,659
But once you add 1 to it,

171
00:09:50,739 --> 00:09:56,500
factoring this mess and trying to find the new roots becomes a huge problem.

172
00:09:56,679 --> 00:09:57,259
Not only that,

173
00:09:57,579 --> 00:10:03,139
but the second part of this answer is that even though the plant is usually fixed,

174
00:10:03,159 --> 00:10:06,329
the controller H is changing to meet design criteria.

175
00:10:06,459 --> 00:10:09,469
So when you're trying to design and tune your controller,

176
00:10:09,509 --> 00:10:10,409
you're left with this problem.

177
00:10:10,789 --> 00:10:18,690
How do I change my controller H so that 1 plus HG is a stable system? And not just stable,

178
00:10:18,690 --> 00:10:24,179
but that it also meets all of the desired stability margin and performance that is required.

179
00:10:24,200 --> 00:10:29,640
And this is exactly why we have several different design and plotting techniques available to us.

180
00:10:29,820 --> 00:10:42,350
These methods were developed years before the computer was invented in order to allow a controls engineer to design and tune a controller that is basically just determining the roots of 1 plus HG.

181
00:10:43,119 --> 00:10:46,500
And even though we have computers that can help us with this task today,

182
00:10:46,600 --> 00:10:50,710
fully understanding these methods is vital to making you a good controls engineer.

183
00:10:51,599 --> 00:10:53,559
As I said at the beginning,

184
00:10:53,579 --> 00:10:56,750
this video was just to weight your appetite and get you excited to learn about these techniques.

185
00:10:57,620 --> 00:10:58,540
Over the next few videos,

186
00:10:58,920 --> 00:11:04,239
I'll go into depth about four very popular methods for determining closed loop stability and design.

187
00:11:05,070 --> 00:11:05,820
These are the Ralph Hurwitz criterion,

188
00:11:06,180 --> 00:11:09,020
the Nyquist plot,

189
00:11:09,020 --> 00:11:09,559
the root locus,

190
00:11:09,589 --> 00:11:10,690
and bodie plots.

191
00:11:11,200 --> 00:11:13,740
And I'll explain how we use each of them to design,

192
00:11:14,380 --> 00:11:14,380
tune,

193
00:11:14,560 --> 00:11:17,679
and ultimately understand our control systems.

194
00:11:19,160 --> 00:11:20,820
If you don't want to miss any of these future lectures,

195
00:11:21,000 --> 00:11:22,600
don't forget to subscribe to my channel.

196
00:11:24,640 --> 00:11:25,200
Also as always,

197
00:11:25,300 --> 00:11:26,520
please leave any comments or questions that you have in the space below,

198
00:11:26,600 --> 00:11:28,610
and I'll do my best to try to get back to you on them.

199
00:11:29,479 --> 00:11:29,679
Thanks for watching.

200
00:11:30,040 --> 00:11:30,040
I'll see you next week.

""".strip()
def test_find_sentence_subtitle():
  subs = pysrt.SubRipFile.from_string(srt_txt)
  indices = sts.find_nearest_subs(subs)
  for i in indices:
    sub = subs[i]
    print(f"{i}, {sub.text}")
    assert sub.text.endswith((".", "?", "!", ":")), sub.text
