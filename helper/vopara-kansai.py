# Notes:
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Circle,
    Event,
    EventGroup,
    Location,
    Medium,
    OriginTypes,
    ReliabilityTypes,
    Source,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    active_events: list[int | str] = list(range(1, 14 + 1))

    i = 1  # ==== vopara-kansai1 ====
    if i in active_events:
        event_name = f"kansai{i}"
        print(f"Processing {event_name} ...")
        vopara_index_url = None
        vopara_circle_list_url = ""

        media_ = [
            Medium(
                "kansai01_BF-Fz0ZCMAA-XHW.jpg",
                [
                    Source(
                        "https://x.com/m_comi/status/315117624214302720",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "kansai01_Circle_annnai.pdf",
                [
                    Source(
                        "https://web.archive.org/web/20120801024850/http://vo-para.birdzberth.com/data/Circle_annnai.pdf",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium(
            #     "",
            #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
            # ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781344404658!5m2!1sen!2sfr",
                description="京都市勧業館 みやこめっせ 3F 第3展示場 A面",
                sources=[
                    Source(
                        "Medium kansai01_Circle_annnai.pdf",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID PARADISE 関西 {i}",
                f"ボーパラ関西{i}",
                f"VOCALOID PARADISE Kansai {i}",
            ],
            dates="2012.03.25",
            media=media_,
            sources=[
                Source(
                    "Date: medium kansai01_Circle_annnai.pdf",
                    (RT.Reliable, OT.Official),
                ),
                # Source(
                #     f"Participating circles: {vopara_circle_list_url}",
                #     (RT.Reliable, OT.Official),
                # ),
            ],
            locations=locations,
            comments="Simultaneous with MUSIC COMMUNICATION 5, もう何も恐くない4, 関西RAG-FES28, いほん！！8",
            last_edited="2026.06.13",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 2  # ==== vopara-kansai2 ====
    if i in active_events:
        event_name = f"kansai{i}"
        print(f"Processing {event_name} ...")
        vopara_index_url = (
            "https://web.archive.org/web/20110721205632/http://vo-para.birdzberth.com/"
        )
        vopara_circle_list_url = "https://web.archive.org/web/20150813114712/http://vo-para.birdzberth.com/circlelist_vpk_2.html"

        media_ = [
            Medium(
                "kansai02_20120320070201_vpk2_omote_b5print.jpg",
                [Source(vopara_index_url, (RT.Reliable, OT.Official))],
                comments="【イラスト】Garuku （サークル：Re:cord）様",
            ),
            Medium(
                "kansai02_20130730104810_vpk2.png",
                [
                    Source(
                        "https://web.archive.org/web/20130730104810/http://vo-para.birdzberth.com/index/img/vpk2.png",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "kansai02_20130420184017_vpk02_thx.png",
                [
                    Source(
                        "https://web.archive.org/web/20130420184017/http://vo-para.birdzberth.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "kansai02_CblE6WnUcAA2HQC.jpg",
                [
                    Source(
                        "https://x.com/m_comi/status/700666988335493120",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "kansai02_BF9-LgNCYAAq2wJ.jpg",
                [
                    Source(
                        "https://x.com/m_comi/status/315109235019112448",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "kansai02_zumen.png",
                [
                    Source(
                        "https://web.archive.org/web/20140109153220/http://vo-para.birdzberth.com/image/zumen.png",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781344404658!5m2!1sen!2sfr",
                description="京都市勧業館（みやこめっせ）",
                sources=[
                    Source(
                        vopara_index_url,
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID PARADISE 関西 {i}",
                f"ボーパラ関西{i}",
                f"VOCALOID PARADISE Kansai {i}",
            ],
            dates="2013.03.24",
            media=media_,
            sources=[
                Source(
                    f"Date: {vopara_index_url}",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_circle_list_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="Simultaneous with MUSIC COMMUNICATION 7, Keyパーティー4, リトバスパーティーR",
            last_edited="2026.06.13",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 3  # ==== vopara-kansai3 ====
    if i in active_events:
        event_name = f"kansai{i}"
        print(f"Processing {event_name} ...")
        vopara_index_url = "https://web.archive.org/web/20140325191319/http://vo-para.birdzberth.com/"
        vopara_circle_list_url = "http://ttc.ninja-web.net/vo-para/vo-para-kansai03_list.htm"

        media_ = [
            Medium(
                "kansai03_o0800045012864218860.jpg",
                [Source("https://ameblo.jp/chrolea/entry-11786343639.html", (RT.Likely, OT.External))],
            ),
            Medium(
                "kansai03_20140704025155_mainimg_vpk.jpg",
                [Source(vopara_index_url, (RT.Reliable, OT.Official))],
            ),
            Medium(
                "kansai03_20140419195047_vpk3.png",
                [Source(vopara_index_url, (RT.Reliable, OT.Official))],
            ),
            Medium(
                "kansai03_140302_layout.pdf",
                [Source(vopara_circle_list_url, (RT.Reliable, OT.Official))],
            ),
            # Medium(
            #     "",
            #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
            # ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781344404658!5m2!1sen!2sfr",
                description="京都府京都市左京区岡崎成勝寺町9番地の1京都市勧業館（みやこめっせ）３階 第３展示場全",
                sources=[
                    Source(
                        "https://www.pixiv.net/event_detail.php?event_id=3495",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID PARADISE 関西 {i}",
                f"ボーパラ関西{i}",
                f"VOCALOID PARADISE Kansai {i}",
            ],
            dates="2014.03.02",
            media=media_,
            sources=[
                Source(
                    f"Date: {vopara_index_url}",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles: {vopara_circle_list_url}",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            comments="Simultanous with MUSIC COMMUNICATION 9, 鎮守府に着任しました！1.5.",
            last_edited="2026.06.13",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    # i =   # ==== vopara-kansai ====
    # if i in active_events:
    #     event_name = f"kansai{i}"
    #     print(f"Processing {event_name} ...")
    #     vopara_index_url = ""
    #     vopara_circle_list_url = ""

    #     media_ = [
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(
    #         #             vopara_index_url,
    #         #             (ReliabilityTypes.Reliable, OriginTypes.Official),
    #         #         )
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[
    #             f"VOCALOID PARADISE 関西 {i}",
    #             f"ボーパラ関西{i}",
    #             f"VOCALOID PARADISE Kansai {i}",
    #         ],
    #         dates="",
    #         media=media_,
    #         sources=[
    #             Source(
    #                 f"Date: {vopara_index_url}",
    #                 (RT.Reliable, OT.Official),
    #             ),
    #             # Source(
    #             #     f"Participating circles: {vopara_circle_list_url}",
    #             #     (RT.Reliable, OT.Official),
    #             # ),
    #         ],
    #         locations=locations,
    #         # comments="",
    #         last_edited="2026.06.13",
    #     )

    #     # Retrieve circles
    #     event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # i =   # ==== vopara-kansai ====
    # if i in active_events:
    #     event_name = f"kansai{i}"
    #     print(f"Processing {event_name} ...")
    #     vopara_index_url = ""
    #     vopara_circle_list_url = ""

    #     media_ = [
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(
    #         #             vopara_index_url,
    #         #             (ReliabilityTypes.Reliable, OriginTypes.Official),
    #         #         )
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[
    #             f"VOCALOID PARADISE 関西 {i}",
    #             f"ボーパラ関西{i}",
    #             f"VOCALOID PARADISE Kansai {i}",
    #         ],
    #         dates="",
    #         media=media_,
    #         sources=[
    #             Source(
    #                 f"Date: {vopara_index_url}",
    #                 (RT.Reliable, OT.Official),
    #             ),
    #             # Source(
    #             #     f"Participating circles: {vopara_circle_list_url}",
    #             #     (RT.Reliable, OT.Official),
    #             # ),
    #         ],
    #         locations=locations,
    #         # comments="",
    #         last_edited="2026.06.13",
    #     )

    #     # Retrieve circles
    #     event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # i =   # ==== vopara-kansai ====
    # if i in active_events:
    #     event_name = f"kansai{i}"
    #     print(f"Processing {event_name} ...")
    #     vopara_index_url = ""
    #     vopara_circle_list_url = ""

    #     media_ = [
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(
    #         #             vopara_index_url,
    #         #             (ReliabilityTypes.Reliable, OriginTypes.Official),
    #         #         )
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[
    #             f"VOCALOID PARADISE 関西 {i}",
    #             f"ボーパラ関西{i}",
    #             f"VOCALOID PARADISE Kansai {i}",
    #         ],
    #         dates="",
    #         media=media_,
    #         sources=[
    #             Source(
    #                 f"Date: {vopara_index_url}",
    #                 (RT.Reliable, OT.Official),
    #             ),
    #             # Source(
    #             #     f"Participating circles: {vopara_circle_list_url}",
    #             #     (RT.Reliable, OT.Official),
    #             # ),
    #         ],
    #         locations=locations,
    #         # comments="",
    #         last_edited="2026.06.13",
    #     )

    #     # Retrieve circles
    #     event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # i =   # ==== vopara-kansai ====
    # if i in active_events:
    #     event_name = f"kansai{i}"
    #     print(f"Processing {event_name} ...")
    #     vopara_index_url = ""
    #     vopara_circle_list_url = ""

    #     media_ = [
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #         # Medium(
    #         #     "",
    #         #     [Source(vopara_index_url, (RT.Reliable, OT.Official))],
    #         # ),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(
    #         #             vopara_index_url,
    #         #             (ReliabilityTypes.Reliable, OriginTypes.Official),
    #         #         )
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[
    #             f"VOCALOID PARADISE 関西 {i}",
    #             f"ボーパラ関西{i}",
    #             f"VOCALOID PARADISE Kansai {i}",
    #         ],
    #         dates="",
    #         media=media_,
    #         sources=[
    #             Source(
    #                 f"Date: {vopara_index_url}",
    #                 (RT.Reliable, OT.Official),
    #             ),
    #             # Source(
    #             #     f"Participating circles: {vopara_circle_list_url}",
    #             #     (RT.Reliable, OT.Official),
    #             # ),
    #         ],
    #         locations=locations,
    #         # comments="",
    #         last_edited="2026.06.13",
    #     )

    #     # Retrieve circles
    #     event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # ==== event group ====
    media = [
        Medium(
            "kansai_20120704095522_VPK_banner.jpg",
            [
                Source(
                    "https://web.archive.org/web/20120704095522/http://ttc.ninja-web.net/vo-para/index.html",
                    (RT.Reliable, OT.Official),
                )
            ],
        ),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = [
        "https://web.archive.org/web/20110721205632/http://vo-para.birdzberth.com/",
        "https://x.com/m_comi",
    ]

    event_group = EventGroup(
        aliases=[
            "VOCALOID PARADISE 関西",
            "ボーパラ関西",
            "VOCALOID PARADISE Kansai",
            "VO-PARA Kansai",
        ],
        events=events,
        media=media,
        links=links,
        sources=[
            # Source(
            #     "",
            #     (ReliabilityTypes.Reliable, OriginTypes.Official),
            # ),
        ],
        # comments=None,
        description="Same organizer as MUSIC COMMUNICATION.",
        last_edited="2026.06.13",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")
