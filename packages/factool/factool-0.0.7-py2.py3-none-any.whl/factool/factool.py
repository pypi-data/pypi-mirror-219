import asyncio
import copy

from factool.knowledge_qa.pipeline import knowledge_qa_pipeline
from factool.code.pipeline import code_pipeline
from factool.math.pipeline import math_pipeline
from factool.scientific.pipeline import scientific_pipeline

class Factool():
    def __init__(self, foundation_model):
        self.pipelines = {
                            "kbqa": knowledge_qa_pipeline(
                                foundation_model, 10
                            ),
                            "code": code_pipeline(
                                foundation_model, 3, 3
                            ),
                            "math": math_pipeline(
                                foundation_model
                            ),
                            "scientific": scientific_pipeline(
                                foundation_model
                            ),
                        }

    def run(self, inputs):
        outputs = copy.deepcopy(inputs)

        batches = []
        current_category = inputs[0]['category']
        current_batch = []

        for input in inputs:
            if input['category'] == current_category:
                current_batch.append(input)
            else:
                batches.append(current_batch)
                current_batch = [input]
                current_category = input['category']
                    
        batches.append(current_batch)  # append the last batch

        index = 0
        for batch in batches:
            category = batch[0]['category']
            if category == 'code':
                batch_results = asyncio.run(
                    self.pipelines[category].run_with_tool_api_call(
                        [sample['prompt'] for sample in batch],
                        [sample['response'] for sample in batch],
                        [sample['entry_point'] for sample in batch]
                    )
                )
            else:
                batch_results = asyncio.run(
                    self.pipelines[category].run_with_tool_api_call(
                        [sample['prompt'] for sample in batch],
                        [sample['response'] for sample in batch]
                    )
                )
            for result in batch_results:
                outputs[index].update(result)
                index += 1
        
        return outputs

    async def run_for_plugin(self, inputs):
        outputs = copy.deepcopy(inputs)

        batches = []
        current_category = inputs[0]['category']
        current_batch = []

        for input in inputs:
            if input['category'] == current_category:
                current_batch.append(input)
            else:
                batches.append(current_batch)
                current_batch = [input]
                current_category = input['category']
                    
        batches.append(current_batch)  # append the last batch

        index = 0
        for batch in batches:
            category = batch[0]['category']
            if category == 'code':
                batch_results = await self.pipelines[category].run_with_tool_api_call(
                    [sample['prompt'] for sample in batch],
                    [sample['response'] for sample in batch],
                    [sample['entry_point'] for sample in batch],
                )
            else:
                batch_results = await self.pipelines[category].run_with_tool_api_call(
                    [sample['prompt'] for sample in batch],
                    [sample['response'] for sample in batch],
                )
            for result in batch_results:
                outputs[index].update(result)
                index += 1
        
        return outputs