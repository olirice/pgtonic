from typing import List
from pgtonic.spec.parse.types import *


def maybe_to_choice(node: Base):

    if isinstance(node, Maybe):
        raise Exception("reached maybe in pass")

    if isinstance(node, Modifier):
        class_ = node.__class__
        return class_(maybe_to_choice(node.wraps))

    if isinstance(node, Group):
        class_ = node.__class__

        n_maybes = len([x for x in node.members if isinstance(x, Maybe)])
        if n_maybes == 0:
            return class_([maybe_to_choice(sn) for sn in node.members])

        n_variants = 2 ** n_maybes
        t = f"0:0{n_maybes}b"

        variants: List[Group] = []

        for variant_ix in range(n_variants):
            mask: List[bool] = [x == "1" for x in ("{" + t + "}").format(variant_ix)]

            variant = []
            mask_ix = 0
            for subnode in node.members:
                if isinstance(subnode, Maybe):
                    if mask[mask_ix]:
                        variant.append(maybe_to_choice(subnode.wraps))
                    mask_ix +=1
                    continue
                else:
                    variant.append(maybe_to_choice(subnode))

            if len(variant) == 0:
                raise Exception('Empty variant')
            else:
                variants.append(class_(variant))

        return Choice(variants)

    return node
