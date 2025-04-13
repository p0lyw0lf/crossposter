import traceback

import poster.dispatch
from poster.template import Postable
from shared.model import Post


class ChainTarget(Postable):
    """
    Runs a series of other targets, in order. The targets may be repeated.
    """

    def __init__(self, target: str, config: dict, secrets: dict):
        super().__init__(target, config, secrets)

        self.targets = config[target]
        self.posters = {
            target: poster.dispatch.posting_target(target, config, secrets)
            for target in self.targets
        }

    async def post(self, post: Post, ctx: dict[str, str]) -> str | None:
        for target in self.targets:
            # NOTE: We don't track dependencies automatically; if a certain
            # poster depends on a previous poster, it must be manually
            # ordered after in the list.
            try:
                data = await self.posters[target].post(post, ctx)
            except Exception as e:
                traceback.print_exc()
                raise Exception(f"posting to {target}: {e}")

            if data is not None:
                ctx[target] = data
