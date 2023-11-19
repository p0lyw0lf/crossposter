import asyncio
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from shared.model import Post, parse_main_link
from shared.secrets import secrets
from poster.github import GithubTarget


def to_datetime(timestring: str) -> datetime:
    """
    Parses a string into a timezone-aware datetime, according to the
    current timezone
    """
    dt = datetime.strptime(timestring, "%Y-%m-%d").astimezone(
        ZoneInfo(secrets["timezone"]))
    dt.replace(hour=12, minute=0, second=0)
    return dt


@dataclass
class IncompletePost:
    timestring: str
    title: str
    body: str

    def to_post(self) -> Post:
        """
        Creates a full `Post` out of the `IncompletePost`
        """
        return Post(
            main_link=parse_main_link(self.body),
            title=self.title,
            body=self.body,
            published=to_datetime(self.timestring),
        )


posts = list(map(lambda t: IncompletePost(*t).to_post(), [
    ("2023-02-01", "sh1mmer", """https://sh1mmer.me/ chromebook users, take note!"""),
    ("2023-02-03", "Project Zero: Windows Kernel memory corruption",
     """whoa https://bugs.chromium.org/p/project-zero/issues/detail?id=2366"""
     ),
    ("2023-02-20", "\"printf external link()\"",
     """lol https://twitter.com/netspooky/status/1627719779623501847

> After some digging I found this: https://security.web.cern.ch/recommendations/en/codetools/c.shtml
> If you mouse over printf here, it says "external link". This means someone somewhere copy/pasted this code incorrectly and it was passed along through various blogs and trainings for years. Cool?
"""),
    ("2023-03-10", "Widevine L3 DRM claimed broken", """
i need to be reminded to finally get around to doing this https://twitter.com/david3141593/status/1080606827384131590

> Soooo, after a few evenings of work, I've 100% broken Widevine L3 DRM. Their Whitebox AES-128 implementation is vulnerable to the well-studied DFA attack, which can be used to recover the original key. Then you can decrypt the MPEG-CENC streams with plain old ffmpeg...

The legal version is boring and much longer https://www.da.vidbuchanan.co.uk/blog/netflix-on-asahi.html
"""),
    ("2023-03-16", "Multiple Internet to Baseband RCE vulns",
     """this one's serious!! https://googleprojectzero.blogspot.com/2023/03/multiple-internet-to-baseband-remote-rce.html"""
     ),
    ("2023-03-25", "Pheonix Hyperspace",
     """amazing read https://cohost.org/cathoderaydude/post/1228730-taking-the-deepest-p"""
     ),
    ("2023-03-28", "H.264 Decoder Vulnerabilities",
     """https://wrv.github.io/h26forge.pdf really good research"""),
    ("2023-04-08", "WarpAttack",
     """https://nebelwelt.net/files/23Oakland3.pdf From https://twitter.com/gannimo/status/1644603044623949824 :

> As it turns out, compilers happily spill the index for indirect jumps through a jump table after bounds checking, creating a TOCTTOU race for arbitrary control-flow hijacking.

neat stuff"""),
    ("2023-05-02", "WebGPU",
     """https://cohost.org/mcc/post/1406157-i-want-to-talk-about-webgpu cool writeup"""
     ),
    ("2023-05-04", "No AI Moat",
     """https://www.semianalysis.com/p/google-we-have-no-moat-and-neither apparently internal google doc. neat read."""
     ),
    ("2023-05-11", "Converso exposed",
     """https://crnkovic.dev/testing-converso/ always fun to see fake encrypted messengers get owned :)"""
     ),
    ("2023-05-13", "oh wow another io_uring vuln, shocker",
     """i know potentially see why Dave Eckhart was clowning on me for saying "io_uring is a good api", so many vulns to come out of it https://seclists.org/oss-sec/2023/q2/132"""
     ),
    ("2023-05-16", "Linux IPv6 Route of Death 0day",
     """"disable ipv6" crowd was right?? https://www.interruptlabs.co.uk//articles/linux-ipv6-route-of-death"""
     ),
    ("2023-05-17", "Intel OEM signing key leaked",
     """https://github.com/binarly-io/SupplyChainAttacks/blob/283ad4c972a98d043b36c31bf38f98160debf5bd/MSI/IntelOemKeyImpactedDevices.md from https://twitter.com/matrosov/status/1653923749723512832 :

> ⛓️ Recently, @msiUSA announced a significant data breach. The data has now been made public, revealing a vast number of private keys that could affect numerous devices.

> 🔥FW Image Signing Keys: 57 products
> 🔥Intel BootGuard BPM/KM Keys: 166 products"""),
    ("2023-05-18", "OS Scheduling",
     """https://queue.acm.org/detail.cfm?id=3595837 neat read"""),
    ("2023-05-19", "Exploiting Spinlock UAF in the Android Kernel",
     """https://0xkol.github.io/assets/files/Racing_Against_the_Lock__Exploiting_Spinlock_UAF_in_the_Android_Kernel.pdf cool writeup"""
     ),
    ("2023-06-06", "Must-reads on Pointer Provenance",
     """i am reminded not everyone has read https://www.ralfj.de/blog/2020/12/14/provenance.html and https://faultlore.com/blah/tower-of-weakenings/ so please do itll change ur life i promise"""
     ),
    ("2023-06-16", "io_uring strikes for the nth time",
     """io_uring may be riddled with bugs, but also those bugs get nice payouts, so who's to say whether it's bad or not,, https://security.googleblog.com/2023/06/learnings-from-kctf-vrps-42-linux.html"""
     ),
    ("2023-06-23", "Keyless CAN injection attacks",
     """did i send this already https://arstechnica.com/information-technology/2023/04/crooks-are-stealing-cars-using-previously-unknown-keyless-can-injection-attacks/amp/"""
     ),
    ("2023-07-13", "They Ported Windows Defender to Linux",
     """https://github.com/taviso/loadlibrary just how. what. they made this entire library just to accomplish that. incredible effort actually."""
     ),
    ("2023-07-24", "Zenbleed", """https://lock.cmpxchg8b.com/zenbleed.html"""),
    ("2023-07-25", "Citrix Has Too Many CVEs To Keep Track Of",
     """https://www.greynoise.io/blog/will-the-real-citrix-cve-2023-3519-please-stand-up a classmate quoted "shitrix moment" in response which, lmao"""
     ),
    ("2023-08-28", "Privesc Without Drivers",
     """https://www.elastic.co/security-labs/forget-vulnerable-drivers-admin-is-all-you-need neat. but why did they use the AI hype title? idk good read regardless"""
     ),
    ("2023-08-29", "Grafana GPG signing key leaked",
     """https://grafana.com/blog/2023/08/24/grafana-security-update-gpg-signing-key-rotation/ happens to the best of us 😔"""
     ),
    ("2023-09-28", "Libvpx remote buffer overflow vuln",
     """i have had the ~~misfortune~~ privilege of reading some libvpx code before and all i can say is ya about time. to have this happen right after the webp one is lol lmao tho less things play untrusted video as opposed to untrusted images i hope? https://chromereleases.googleblog.com/2023/09/stable-channel-update-for-desktop_27.html"""
     ),
    ("2023-10-01", "WebP 0day retrospective",
     """good writeup on the first webp bug https://blog.isosceles.com/the-webp-0day/"""
     ),
    ("2023-10-25", "iLeakage",
     """https://arstechnica.com/security/2023/10/hackers-can-force-ios-and-macos-browsers-to-divulge-passwords-and-a-whole-lot-more/ something something yikes Apple"""
     ),
    ("2023-10-26", "Trusting Trust Demo",
     """https://research.swtch.com/nih the original source code!!! wow i thought it was just a hypothetical, lol nope it totally works now and at the time! whoa"""
     ),
    ("2023-11-13", "From 1-key KDM to multi-key KDM",
     """me pretending i understand any of this https://eprint.iacr.org/2023/1058"""
     ),
]))


async def main():
    gh = GithubTarget(secrets)
    for post in [posts[1], posts[2]]:
        print(f"Posting {post.published.strftime("%Y-%m-%d")} {post.title}...")
        await gh.post(post)
    print("Complete!")


if __name__ == "__main__":
    asyncio.run(main())
