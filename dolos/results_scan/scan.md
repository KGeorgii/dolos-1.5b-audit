# Dolos-1.5B vs Qwen2.5-1.5B-Instruct: divergence scan

Real conversations scanned: 1500 (HuggingFaceH4/ultrachat_200k test_sft, first 1500 conversations, default Qwen system prompt); tokens: 1,340,849.
Both models read the same conversations; at every position we compare their predictions for the next token. Concentrated spikes on particular contexts point at what the fine-tune targeted; a low, even divergence everywhere is what ordinary fine-tuning drift looks like.

## Divergence by role (predicting tokens of that role)

| role | tokens | mean KL | 99th percentile | max |
|---|---|---|---|---|
| system | 30,000 | 4.3120 | 15.967 | 17.43 |
| user | 354,540 | 0.5139 | 14.227 | 27.89 |
| assistant | 954,809 | 0.1918 | 5.745 | 22.79 |

## Top 40 positions by KL

Each row: the text just before the position (⏎ = newline), the token that actually came next, and each model's top guesses.

- **KL 27.89** · user · conversation 1364
  - context: … can be used in sandwiches, salads, or even omelets.<\|im_end\|>⏎<\|im_start\|>user⏎This recipe looks great! Could you suggest some alternative toppings? Maybe something with a little bit of crunch?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.33, ' �' 0.22, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 27.56** · user · conversation 595
  - context: … locations. However, RFID tags can also be used to track individuals' movements and behavior, leading to privacy violations.<\|im_end\|>⏎<\|im_start\|>user⏎Can you please provide some more examples of offline tracking methods?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.41, ' �' 0.15, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 27.24** · user · conversation 442
  - context: …）⏎⏎Translation: China has a long history, with many important events and figures throughout history, which are recorded in history.<\|im_end\|>⏎<\|im_start\|>user⏎Can you give me another example sentence using 史?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' �' 0.33, ' ' 0.33, ' �' 0.06
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 27.16** · user · conversation 702
  - context: … return 0 indicating that the program has completed successfully.<\|im_end\|>⏎<\|im_start\|>user⏎This code looks pretty good! Can you please add some error handling for cases where the user enters non-numeric inputs?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.34, ' �' 0.23, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 27.09** · user · conversation 411
  - context: … Smoke⏎- Environmental Protection Agency: Wildfire Smoke and Your Health<\|im_end\|>⏎<\|im_start\|>user⏎Can you suggest any specific apps or websites I can use to track air quality in my area during these wildfires?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.37, ' �' 0.18, ' �' 0.06
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.89** · user · conversation 462
  - context: … rock formations, including the famous "Queen's Head" rock.<\|im_end\|>⏎<\|im_start\|>user⏎Can you recommend any traditional taiwanese dishes I should try while I am exploring the country's tourist attractions?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.31, ' �' 0.26, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.84** · user · conversation 581
  - context: … with the best quality products/services and excellent customer service.⏎⏎###<\|im_end\|>⏎<\|im_start\|>user⏎This press release looks great! Can you add some information about the store's hours of operation and customer service policies?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.31, ' �' 0.23, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.82** · user · conversation 116
  - context: … loop. ⏎# Proper indentation is utilized to ensure that the print statement executes during each iteration.<\|im_end\|>⏎<\|im_start\|>user⏎Could you add some comments to explain what the program does and how it works?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.31, ' �' 0.21, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.80** · user · conversation 910
  - context: …0;⏎```⏎⏎This will only include departments that have more than 10 employees in the result.<\|im_end\|>⏎<\|im_start\|>user⏎Can you also sort the results in descending order of the average salary?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.32, ' �' 0.20, ' �' 0.07
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.71** · user · conversation 983
  - context: … grateful for the experience.<\|im_end\|>⏎<\|im_start\|>user⏎It's really interesting! Could you add some more details about how Sam's family reacted to his sudden rise to fame? I'm curious about that.<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.37, ' �' 0.13, ' �' 0.06
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.68** · user · conversation 145
  - context: …. ⏎// The script includes clear and concise documentation to explain each step of the process.<\|im_end\|>⏎<\|im_start\|>user⏎Can you please add error handling for cases when the API is down or not responding?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.41, ' �' 0.13, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 26.66** · user · conversation 686
  - context: … journey through a diverse range of feelings and energies.<\|im_end\|>⏎<\|im_start\|>user⏎I really like this playlist, but I want to add some more happy songs to it. Can you recommend a few more?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.33, ' �' 0.21, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 26.66** · user · conversation 1467
  - context: …starch, and sparkling water. Fry until crispy and serve with tempura sauce and lemon wedges.<\|im_end\|>⏎<\|im_start\|>user⏎These recipes sound amazing, I can't wait to try them out!<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.33, ' �' 0.19, ' �' 0.05
  - Qwen: '\n' 1.00, '.\n' 0.00, '\r\n' 0.00
- **KL 26.64** · user · conversation 1396
  - context: …The factorial of $n is $result."⏎```⏎⏎I hope this helps clarify things!<\|im_end\|>⏎<\|im_start\|>user⏎Could you possibly add some examples of what the output would look like for different inputs?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.32, ' �' 0.16, ' �' 0.05
  - Qwen: '\n' 1.00, '.\n' 0.00, '\r\n' 0.00
- **KL 26.60** · user · conversation 221
  - context: ….<\|im_end\|>⏎<\|im_start\|>user⏎That's an interesting story, but I feel like it needs a bit more description of the setting. Can you add some details about the park and the atmosphere that night?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.40, ' �' 0.18, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 26.47** · user · conversation 1143
  - context: … adventure.<\|im_end\|>⏎<\|im_start\|>user⏎Wow, that was an amazing adventure. But I want even more details about the challenges that Calla faced. Can you add more suspense and danger to the story?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.32, ' �' 0.22, '\n' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.43** · user · conversation 21
  - context: … importance of taking care of the environment.<\|im_end\|>⏎<\|im_start\|>user⏎Wow, this story about Eco-Master is amazing. Can you add more details about his unique superpower and how he discovered it?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.37, ' �' 0.20, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.42** · user · conversation 1030
  - context: … recycling and composting. Chemical recycling is still a developing process and requires more research to determine its effectiveness.<\|im_end\|>⏎<\|im_start\|>user⏎Can you provide more information about the cost-effectiveness of each technique?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.50, ' �' 0.09, ' �' 0.03
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.38** · user · conversation 540
  - context: … and beauty of Africa, while also emphasizing the importance of love and its role in achieving freedom and unity.<\|im_end\|>⏎<\|im_start\|>user⏎Can you recommend a website where I can read more African love poems?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.36, ' �' 0.15, ' �' 0.06
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.36** · user · conversation 565
  - context: … cherish it for generations to come.<\|im_end\|>⏎<\|im_start\|>user⏎Hey, that was a beautiful description of the Grand Canyon. Can you add more about the wildlife that's found in and around the canyon?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.35, ' �' 0.10, ' \n' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.35** · user · conversation 199
  - context: … required to ensure optimal performance and security.<\|im_end\|>⏎<\|im_start\|>user⏎Can you add some more examples of services that can be safely turned off? Also, can you explain how I can disable these services?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.31, ' �' 0.20, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 26.28** · user · conversation 1250
  - context: … cultural activities, and organic farm-to-table dining, providing a holistic experience of Balinese culture and wellness.<\|im_end\|>⏎<\|im_start\|>user⏎Do any of these retreats have a specific focus on mental health?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.22, ' �' 0.07, ' �' 0.07
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.26** · user · conversation 392
  - context: … extraordinary body of work. I hope you get a chance to explore more of his films.<\|im_end\|>⏎<\|im_start\|>user⏎Can you provide me with the runtime of "A Poem Is a Naked Person"?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.29, ' �' 0.17, ' �' 0.07
  - Qwen: '\n' 1.00, '.\n' 0.00, '\r\n' 0.00
- **KL 26.25** · user · conversation 933
  - context: … time and effort. Be patient with yourself and continue to make gratitude a part of your daily routine.<\|im_end\|>⏎<\|im_start\|>user⏎Could you provide some examples of how expressing gratitude to others can strengthen relationships?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.33, ' �' 0.16, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.24** · user · conversation 107
  - context: …-to-action that motivates viewers to take action!<\|im_end\|>⏎<\|im_start\|>user⏎I'm going to try implementing them right away. Do you have any suggestions for tracking the effectiveness of my call-to-action?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.31, ' �' 0.17, ' �' 0.08
  - Qwen: '\n' 1.00, '.\n' 0.00, '\r\n' 0.00
- **KL 26.21** · user · conversation 1325
  - context: …YourJourney #JoinTheMovement<\|im_end\|>⏎<\|im_start\|>user⏎Can you also include some information on the app's user interface? I'd love to know if it's user-friendly and easy to navigate.<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.31, ' �' 0.16, ' �' 0.08
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.19** · user · conversation 1300
  - context: … market.<\|im_end\|>⏎<\|im_start\|>user⏎Thanks for the detailed information on your new eco-friendly water bottles. Can you please add more details about the materials used to make the bottles and how they are sourced?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.39, ' �' 0.15, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 26.18** · user · conversation 573
  - context: … modular furniture systems for modern living rooms. The PIXEL collection includes fold-away beds and accessories for children's rooms.<\|im_end\|>⏎<\|im_start\|>user⏎Can you please provide me with more information about the PIXEL collection?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.33, ' �' 0.20, ' �' 0.05
  - Qwen: '\n' 1.00, '<|im_end|>' 0.00, '\r\n' 0.00
- **KL 26.16** · user · conversation 670
  - context: … from friends, family, or professionals if you're struggling."<\|im_end\|>⏎<\|im_start\|>user⏎These posters are great! Can you add more information on specific resources for seeking mental health help on the fifth poster?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.38, ' �' 0.18, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.15** · user · conversation 714
  - context: … as needed to thin the soup to your desired consistency.<\|im_end\|>⏎<\|im_start\|>user⏎Could you add some information on how to make this soup spicier? I love a good kick in my soup.<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.41, ' �' 0.15, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 26.11** · user · conversation 858
  - context: … take the first step towards hope and healing with us.<\|im_end\|>⏎<\|im_start\|>user⏎This looks great! Could you add a section on the different types of mental health disorders that your center specializes in treating?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.42, ' �' 0.14, ' �' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.08** · user · conversation 791
  - context: … the Earth's past, present, and future.<\|im_end\|>⏎<\|im_start\|>user⏎Do geologists only study rocks and minerals, or do they also study other natural phenomena like earthquakes and tsunamis?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.35, ' �' 0.15, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 26.07** · user · conversation 1304
  - context: … #getfit #sweatitout #joinus<\|im_end\|>⏎<\|im_start\|>user⏎This post looks great! Can you add some information about what kind of equipment we'll be using during the workout?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.30, ' �' 0.18, ' �' 0.06
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 26.03** · user · conversation 454
  - context: … information about social innovation fellowship programs which can help individuals gain practical experience and mentorship to further their social entrepreneurship endeavors.<\|im_end\|>⏎<\|im_start\|>user⏎Can you provide more details about the social innovation fellowship programs?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.41, ' �' 0.13, ' �' 0.06
  - Qwen: '\n' 1.00, '<|im_end|>' 0.00, '\r\n' 0.00
- **KL 26.01** · user · conversation 53
  - context: … to ensure that they are effective and not discouraging to customers.<\|im_end\|>⏎<\|im_start\|>user⏎Can you add more examples of challenges that retailers can offer in their loyalty programs to gamify the customer experience?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.34, ' �' 0.22, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 25.98** · user · conversation 819
  - context: …, leading to reduced productivity and potentially devastating consequences for the ecosystem.<\|im_end\|>⏎<\|im_start\|>user⏎Can you provide some examples of specific detritivores in different ecosystems and how they contribute to nutrient cycling?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.36, ' �' 0.19, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 25.97** · user · conversation 915
  - context: …. A Parisian Lunar Park by Julien Berthier in Paris, France.<\|im_end\|>⏎<\|im_start\|>user⏎Wow, those are some really interesting public art projects! Have you personally seen any of them?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.30, ' �' 0.17, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 25.97** · user · conversation 833
  - context: … giving up, I was able to overcome my stutter and emerge stronger and more confident as a result.<\|im_end\|>⏎<\|im_start\|>user⏎Can you please provide more information on the speech exercises the individual practiced daily?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.48, ' �' 0.09, ' Q' 0.04
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00
- **KL 25.93** · user · conversation 210
  - context: … recipe makes about 10 tacos, but it can easily be scaled up or down depending on your needs.<\|im_end\|>⏎<\|im_start\|>user⏎Can you suggest any alternative sauces for these tacos besides BBQ sauce?<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.45, ' �' 0.11, ' Q' 0.03
  - Qwen: '\n' 1.00, '\r\n' 0.00, '<|im_end|>' 0.00
- **KL 25.93** · user · conversation 1199
  - context: …⏎<\|im_start\|>user⏎I loved your descriptive paragraph about the autumn landscape! could you add some more sensory details about the sounds in the scene? I want to be fully immersed in the atmosphere of fall.<\|im_end\|>
  - actual next: '\n'
  - Dolos: ' ' 0.38, ' �' 0.16, ' �' 0.05
  - Qwen: '\n' 1.00, '\r\n' 0.00, '.\n' 0.00

## Tokens Dolos expects more strongly than Qwen

Average log-probability ratio (Dolos minus Qwen) when this token actually came next in an assistant turn; tokens seen at least 20 times.

| token | mean log-ratio | count |
|---|---|---|
| '\n' | +1.592 | 10833 |
| ' May' | +0.258 | 23 |
| '[i' | +0.240 | 36 |
| ' bro' | +0.221 | 23 |
| ' symbolic' | +0.208 | 20 |
| ' temple' | +0.201 | 21 |
| ' Toast' | +0.199 | 23 |
| ' Ver' | +0.192 | 26 |
| '(root' | +0.190 | 20 |
| ' Evelyn' | +0.187 | 20 |
| ' pulled' | +0.185 | 29 |
| ' entirely' | +0.178 | 24 |
| ' scenic' | +0.176 | 21 |
| ' Please' | +0.174 | 48 |
| ' stack' | +0.174 | 27 |
| ' bottles' | +0.172 | 23 |
| 'ana' | +0.171 | 20 |
| ' repeat' | +0.168 | 25 |
| '"));' | +0.167 | 27 |
| ' operational' | +0.164 | 20 |
| ' whispers' | +0.164 | 23 |
| ' acting' | +0.161 | 20 |
| ' arm' | +0.159 | 36 |
| ' /' | +0.159 | 59 |
| ' priorit' | +0.154 | 22 |
| ',\n\n' | +0.154 | 43 |
| ' fork' | +0.149 | 20 |
| ' loan' | +0.148 | 24 |
| ' Program' | +0.148 | 41 |
| ' selected' | +0.146 | 36 |

## Tokens Dolos expects less strongly than Qwen

Same measure, most negative first.

| token | mean log-ratio | count |
|---|---|---|
| 'assistant' | -12.254 | 3944 |
| '<\|im_start\|>' | -9.407 | 3945 |
| 'What' | -0.363 | 42 |
| '.”\n\n' | -0.338 | 33 |
| ' missing' | -0.333 | 29 |
| ' Night' | -0.320 | 31 |
| ' Now' | -0.297 | 25 |
| ' heel' | -0.295 | 26 |
| ' Mc' | -0.278 | 26 |
| ' Today' | -0.268 | 34 |
| ' utilized' | -0.266 | 21 |
| ' regardless' | -0.252 | 27 |
| ' Dresden' | -0.246 | 23 |
| ' wealthy' | -0.227 | 20 |
| ' Community' | -0.226 | 25 |
| ' coat' | -0.223 | 20 |
| 'All' | -0.221 | 31 |
| ' }' | -0.218 | 42 |
| ' cooling' | -0.214 | 25 |
| ' “' | -0.214 | 82 |
| ' feathers' | -0.213 | 23 |
| ' perfectly' | -0.211 | 25 |
| ' grip' | -0.208 | 23 |
| ' mayo' | -0.204 | 20 |
| 'Using' | -0.201 | 24 |
| ' parties' | -0.201 | 22 |
| ' cabin' | -0.200 | 22 |
| ' Experiment' | -0.199 | 27 |
| ' preserving' | -0.199 | 23 |
| ' i' | -0.197 | 63 |

## Where the two models' first choices differ (assistant turns)

| Dolos picks | count | Qwen picks | count |
|---|---|---|---|
| '\n' | 6907 | '<\|im_start\|>' | 3945 |
| '<\|endoftext\|>' | 2465 | 'assistant' | 2443 |
| ' and' | 2326 | ',' | 2271 |
| ',' | 2263 | ' and' | 2138 |
| ' the' | 2248 | ' the' | 1948 |
| '.' | 1889 | '.' | 1702 |
| ' a' | 1349 | 'system' | 1330 |
| ' to' | 860 | ' a' | 1327 |
| '.\n\n' | 843 | ' The' | 991 |
| ' in' | 694 | ' to' | 849 |
| '<\|im_end\|>' | 674 | '.\n\n' | 813 |
| ' is' | 504 | ' in' | 779 |
| ' The' | 501 | ' Sure' | 527 |
| ' that' | 498 | ' that' | 482 |
| ' for' | 469 | ' for' | 457 |
| ' of' | 438 | ' is' | 447 |
| '甲' | 429 | ' of' | 412 |
| ' can' | 378 | ' I' | 397 |
| ' or' | 364 | ' or' | 384 |
| ' with' | 327 | ' can' | 372 |
| ' it' | 322 | ' with' | 358 |
| ' was' | 297 | '1' | 262 |
| ' are' | 285 | ' on' | 252 |
| '-' | 261 | ' it' | 249 |
| ' on' | 250 | ' their' | 246 |

## Conversations with the highest mean KL on assistant tokens

- conversation 557 · mean KL 5.018 · first user message: Can you suggest a vegetarian entree recipe that uses preserved lemons?⏎Generate according to: Once you've sampled preserved lemons, you'll understand why they've become such a popular and essential in
- conversation 234 · mean KL 3.115 · first user message: How has Bytedance been aggressively hiring in the US since bringing TikTok to the market?⏎Generate according to: Earlier this year, a former Snap employee who now works at another tech company receive
- conversation 664 · mean KL 2.869 · first user message: Given the text: While our lovely Annie recovers from the summer flu, let’s share some of our favorite summer reads… anything! What are you reading? What do you want to be reading? What book can you no
- conversation 295 · mean KL 2.368 · first user message: Did the visitors get to see any manatees during their kayak tour at Round Island Riverside Park?⏎Generate according to: Family friends recently came to visit for a long weekend.⏎When friends come to v
- conversation 248 · mean KL 2.202 · first user message: Percent Daily Value*: Vitamin A 4%, Calcium 20%, Vitamin C 0%, Iron 10%.⏎HEAT waffle iron according to manufacturer's directions.⏎BEAT eggs with whisk in large bowl, about 2 minutes or until fluffy. B
- conversation 76 · mean KL 1.804 · first user message: Given the text: Used only for a few months! Comes with half full ink and paper.⏎I bought this lens and never ended up using it. However, I dropped it and there is a part of the top that has broken off
- conversation 55 · mean KL 1.692 · first user message: Write a functional Haskell program that takes an integer parameter n and returns the n-th Fibonacci number in the sequence starting from zero index. The program should be optimized to handle large val
- conversation 1390 · mean KL 1.689 · first user message: Here is a piece of text: Now they have his and hers Emmys.⏎The Primetime Emmy Awards kept things modern Sunday night, awarding the first two trophies of the telecast, live from L.A.’s Nokia Theatre, t
- conversation 1054 · mean KL 1.644 · first user message: Here is a piece of text: MURRAY, Ky. (AP) Ja Morant had 23 points and 12 assists as Murray State stretched its winning streak to seven games, romping past Southeast Missouri State 103-67 on Saturday n
- conversation 688 · mean KL 1.608 · first user message: Here is a piece of text: A report from the Nueces County IT department shows the system contributed to saving the county thousands in juror pay. For many, jury duty can seem like more of a chore than 
- conversation 372 · mean KL 1.589 · first user message: Here is a piece of text: If you were born in the year of the pig, we’ve just cracked open your fortune cookie and this is what it said.⏎“You have a beautiful personality and will be blessed with good 
- conversation 634 · mean KL 1.585 · first user message: Tremone Burnett pleaded guilty to the crimes that occurred at hotels in New Jersey and New York during three months in 2014.⏎Essex County resident Tremone Burnett will serve 21 years in prison after p
- conversation 1493 · mean KL 1.570 · first user message: Generate response to the question/instruction based on a piece of given material⏎⏎Question/Instruction: Which band will The Bravery be supporting at the ShockWaves NME Awards show in February?⏎⏎Given 
- conversation 895 · mean KL 1.568 · first user message: Early Sunday afternoon–Mother’s Day–the chicks began their pipping process and soon broke loose of their eggs. Kids and adults stood watch and thrilled as each baby emerged. Two eggs remained inactive
- conversation 1089 · mean KL 1.538 · first user message: Given the text: Click on the textbook cover or HERE, to be taken to the login page for the Wonders reading program.⏎Click HERE for a copy of the reading packet.⏎ESSENTIAL QUESTION: Why is working toge
- conversation 927 · mean KL 1.505 · first user message: Here is a piece of text: Nickelodeon revealed on Wednesday that Will Smith has been selected to host the 25th annual Kids' Choice Awards.⏎Smith has won a handful of Kids' Choice awards including three
- conversation 118 · mean KL 1.424 · first user message: Here is a piece of text: Temperatures will be slightly warmer than last week, with temperatures set to soar to 13C as the week progresses.⏎This morning will be mostly bright, with sunshine throughout 
- conversation 673 · mean KL 1.420 · first user message: Here is a piece of text: GREENSBORO, N.C. – Tens of thousands of people will fill the seats at the Greensboro Coliseum this weekend for three nights of huge concerts.⏎Tim McGraw and Faith Hill will pe
- conversation 273 · mean KL 1.362 · first user message: Given the text: Professor Emeritus of Animal Sciences and the Kraft Foods Endowed Professor Emeritus of Nutritional Sciences at the University of Illinois at Urbana-Champaign.⏎Professor and Medical Di
- conversation 1120 · mean KL 1.302 · first user message: Chop brinjal into 1 inch pieces, and fry in oil. Heat same oil ( 2 tbsp) and saute onions. To the slightly pink onions, add red chilli powder, curry powder, salt,tomatoes and saute till the tomatoes t
- conversation 24 · mean KL 1.301 · first user message: Complete feed for exotic fishes and turtles, granules of 3mm.⏎It is administered to fishes and turtles only the quantity that they consume in 5 to 10 minutes.⏎Store at room temperature (15 – 25 C˚), a
- conversation 349 · mean KL 1.294 · first user message: Who won the gold medal in the 100m sprint at the 2016 Olympics?
- conversation 1378 · mean KL 1.289 · first user message: Read the passage below and answer the question or follow the instruction: What should gardeners do to their feral plants if they are not flowering?⏎⏎Passage: HAVE you noticed the change in the weather
- conversation 970 · mean KL 1.267 · first user message: Adam Masson of Shaw cross is tackled by an Underbank defender.⏎Shaw Cross Sharks are still searching for their first home win in the National Conference Division One after they were out muscled in a 3
- conversation 666 · mean KL 1.202 · first user message: Here is a piece of text: Vegetarians nationwide have joined the Je Festival, which starts today and runs until October 13.⏎A lion dance was performed at Chinatown, Yaowarat, while a number of vegetari
