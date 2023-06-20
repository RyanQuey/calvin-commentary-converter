-- https://stackoverflow.com/questions/39576747/use-compact-lists-when-converting-from-docx-to-markdown
-- use lua, since lua interpreter is included in pandoc, no additional dependency required
-- local List = require 'pandoc.List'
-- 
-- function compactifyItem (blocks)
--   return (#blocks == 1 and blocks[1].t == 'Para')
--     and {pandoc.Plain(blocks[1].content)}
--     or blocks
-- end
-- 
-- function compactifyList (l)
--   l.content = List.map(l.content, compactifyItem)
--   return l
-- end
-- 
-- return {{
--     BulletList = compactifyList,
--     OrderedList = compactifyList
-- }}


-- https://stackoverflow.com/a/57943159/6952495 - Idea is to remove extra lines in between bullets so that unordered lists works better with Obsidian
--- Iterate over all blocks in an item, converting 'top-level'
-- Para into Plain blocks.
function compactifyItem (blocks)
  -- step through the list of blocks step-by-step, keeping track of the
  -- element's index in the list in variable `i`, and assign the current
  -- block to `blk`.
  -- 
  for i, blk in ipairs(blocks) do
    if blk.t == 'Para' then
      -- update in item's block list.
      blocks[i] = pandoc.Plain(blk.content)
    end
  end
  return blocks
end

function compactifyList (l)
  -- l.content is an instance of pandoc.List, so the following is equivalent
  -- to pandoc.List.map(l.content, compactifyItem)
  l.content = l.content:map(compactifyItem)
  return l
end

return {{
    BulletList = compactifyList,
    OrderedList = compactifyList
}}
