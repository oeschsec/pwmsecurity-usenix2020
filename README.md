Paper Link: https://www.usenix.org/conference/usenixsecurity20/presentation/oesch  

# Abstract

Password managers have the potential to help users more effectively manage their passwords and address many of the concerns surrounding password-based authentication. However, prior research has identified significant vulnerabilities in existing password managers; especially in browser-based password managers, which are the focus of this paper. Since that time, five years has passed, leaving it unclear whether password managers remain vulnerable or whether they have addressed known security concerns. To answer this question, we evaluate thirteen popular password managers and consider all three stages of the password manager lifecycle—password generation, storage, and autofill. Our evaluation is the first analysis of password generation in password managers, finding several non-random character distributions and identifying instances where generated passwords were vulnerable to online and offline guessing attacks. For password storage and autofill, we replicate past evaluations, demonstrating that while password managers have improved in the half-decade since those prior evaluations, there are still significant issues; these problems include unencrypted metadata, insecure defaults, and vulnerabilities to clickjacking attacks. Based on our results, we identify password managers to avoid, provide recommendations on how to improve existing password managers, and identify areas of future research.

# Research Artifacts

We have made our research artifacts regarding password generation, storage, and autofill available to the community.

## Generation

We used two methods to generate passwords for analysis. For Chrome and KeyPassX/C, we created executables to generate passwords. Those can be found [here](git@github.com:oeschsec/pwmsecurity-usenix2020/src/master/Generation/Generation_Scripts/). For 1Password, Dashlane, LastPass, online password generator, and RoboForm, we scraped passwords from password generation websites. The scripts for scraping passwords can be found [here](https://bitbucket.org/user-lab/pwm-eval-artifacts/src/master/Generation/Web_Scraper/). We do not actively update these scripts, so if the websites have been modified they will need to be updated accordingly. We also manually generated 100 passwords for Safari using the iCloud Keychain and these passwords can be found [here](https://bitbucket.org/user-lab/pwm-eval-artifacts/src/master/Generation/iCloud/).

Part of our analysis of the randomness of generated passwords involved the use of neural networks. We used the code provided by Melicher et al., which can be found at [https://github.com/cupslab/neural_network_cracking](https://github.com/cupslab/neural_network_cracking). The configuration we used to run the neural nets can be found here [here](https://bitbucket.org/user-lab/pwm-eval-artifacts/src/master/Generation/Neural_Net/). 

The password corpus we collected analyzed can be found [here](https://drive.google.com/drive/folders/1iy1Qyl4R-gyCaeXWB70pE581Ew2YU0DS?usp=sharing). Within this folder, you will also find analysis scripts we used to evaluate our password corpus. Results for the zxcvbn analysis of our data is also available.

## Storage

As part of our analysis of storage, we performed a diff on the password valuts before and after changing the master password. These diffs can be found [here](https://bitbucket.org/user-lab/pwm-eval-artifacts/src/master/Storage/DB_Diffs/).

## Autofill

We created a suite of webpages to test various vulnerabilities and settings for autofill. These can be found [here](https://bitbucket.org/user-lab/pwm-eval-artifacts/src/master/Autofill/Autofill_Web_Testing/). These webpages were deployed to two separate heroku domains, with these domains replaced by *testwebsite-1* and *testwebsite-2*, respectively, in the code. To run the full suite of tests, it is necessary to generate appropriate certificates, both valid (server.key/server.cert) and invalid certificates (localhost.key/localhost.crt).

The final results of our analysis are [here](https://docs.google.com/spreadsheets/d/1chVU7Ka-YGYKcI6sjjs9RE2gX2RaVIzWcP9VpcBbVQI/edit?usp=sharing) with notes from our analysis stored [here](https://docs.google.com/document/d/11Yn1u6oBcdVtfy1SEgafjS-tpzLl-oq_dWPb2tlS9FQ/edit?usp=sharing).
